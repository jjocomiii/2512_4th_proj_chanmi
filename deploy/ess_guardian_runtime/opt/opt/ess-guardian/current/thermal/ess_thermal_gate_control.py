#!/usr/bin/env python3
import os, json, time
from datetime import datetime, timezone, timedelta

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String

import paho.mqtt.client as mqtt

# ---- ROS topics (override via env) ----
CTRL_TOPIC = os.getenv("ESS_THERM_CTRL_TOPIC", "/ess/request/id")
CAP_TOPIC  = os.getenv("ESS_THERM_CAP_TOPIC",  "/ess/thermal/ack")
EVT_TOPIC  = os.getenv("ESS_THERM_EVT_TOPIC",  "/ess/thermal/events")

# Thermal daemon output (MLX90640 status json)
STATUS_JSON = os.getenv("ESS_THERM_STATUS_JSON", "/var/log/ess-thermal-status.json")

# ---- MQTT ----
MQTT_HOST = os.getenv("ESS_MQTT_HOST", "10.10.14.109")
MQTT_PORT = int(os.getenv("ESS_MQTT_PORT", "1883"))

# 기존 디버그 토픽 유지
TOPIC_THERM = os.getenv("ESS_MQTT_TOPIC_THERM", "ess/thermal/alert")
# ✅ DB 적재용: 서버 backend가 구독하는 토픽
TOPIC_ALERT = os.getenv("ESS_MQTT_TOPIC_ALERT", "ess/alert")

# DB location 필터용
LOCATION = os.getenv("ESS_LOCATION", "robot_1")

WARN_C = float(os.getenv("THERM_WARN_C", "35"))
CRIT_C = float(os.getenv("THERM_CRIT_C", "50"))

# 같은 레벨이면 너무 자주 발행하지 않게(초 단위)
COOLDOWN_SEC = float(os.getenv("THERM_ALERT_COOLDOWN_SEC", "2.0"))

def now_iso():
    kst = timezone(timedelta(hours=9))
    return datetime.now(kst).isoformat(timespec="seconds")

def read_max_c(path: str):
    """
    /var/log/ess-thermal-status.json 에서 최대온도(max)를 읽는다.
    여러 키 이름을 최대한 수용.
    """
    try:
        with open(path, "r") as f:
            d = json.load(f)
        for k in ("max", "max_c", "tmax", "max_temp", "maxC"):
            if k in d and d[k] is not None:
                return float(d[k])
        # 혹시 nested 형태면 여기에 추가로 파싱 로직을 붙이면 됨
        return None
    except Exception:
        return None

class ThermalGate(Node):
    def __init__(self):
        super().__init__("thermal_gate_control")

        self.pub_cap = self.create_publisher(Int32, CAP_TOPIC, 10)
        self.pub_evt = self.create_publisher(String, EVT_TOPIC, 10)
        self.sub_ctrl = self.create_subscription(Int32, CTRL_TOPIC, self.on_ctrl, 10)

        self.last_level = None
        self.last_ts = 0.0

        self.mqtt = mqtt.Client(client_id="thermal_gate_control")
        self.mqtt.on_connect = self._on_mqtt_connect
        self.mqtt.on_disconnect = self._on_mqtt_disconnect
        self.mqtt.connect_async(MQTT_HOST, MQTT_PORT, keepalive=30)
        self.mqtt.loop_start()

        self.get_logger().info(
            f"gate start: ctrl={CTRL_TOPIC}, cap={CAP_TOPIC}, evt={EVT_TOPIC}, "
            f"warn={WARN_C}, crit={CRIT_C}, mqtt={MQTT_HOST}:{MQTT_PORT}, "
            f"therm_topic={TOPIC_THERM}, alert_topic={TOPIC_ALERT}, status={STATUS_JSON}, location={LOCATION}"
        )

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        self.get_logger().info(f"mqtt connected rc={rc}")

    def _on_mqtt_disconnect(self, client, userdata, rc):
        self.get_logger().warn(f"mqtt disconnected rc={rc}")

    def _publish(self, n: int, max_c: float, level: str):
        # (A) 기존 디버그 토픽: ess/thermal/alert
        therm_payload = {"n": int(n), "max": float(max_c), "level": level}
        self.mqtt.publish(TOPIC_THERM, json.dumps(therm_payload), qos=1, retain=False)

        # (B) ✅ DB 토픽: ess/alert (서버 backend 스키마에 맞춤)
        db_payload = {
            "event_type": "thermal",
            "level": level,
            "value": float(max_c),
            "location": LOCATION,
            "message": f"THERMAL {level.upper()}",
            # ts는 서버에서 기본값 처리하는 경우가 많아 옵션. 필요하면 backend에 맞춰 켜도 됨.
            "ts": now_iso(),
        }
        self.mqtt.publish(TOPIC_ALERT, json.dumps(db_payload, ensure_ascii=False), qos=1, retain=False)

    def on_ctrl(self, msg: Int32):
        n = int(msg.data)
        self.get_logger().info(f"queued control n={n}")

        max_c = read_max_c(STATUS_JSON)

        # ROS ack: "처리했다" 의미로 1
        ack = Int32()
        ack.data = 1
        self.pub_cap.publish(ack)

        # ROS events: 진단용
        evt = {"n": n, "max": max_c, "ts": now_iso()}
        evt_msg = String()
        evt_msg.data = json.dumps(evt, ensure_ascii=False)
        self.pub_evt.publish(evt_msg)

        if max_c is None:
            return

        # 위험일 때만 발행
        if max_c >= CRIT_C:
            level = "critical"
        elif max_c >= WARN_C:
            level = "warning"
        else:
            # 정상 온도면 발행 안 함
            self.last_level = None
            return

        # 중복/폭주 방지
        now = time.time()
        if level == self.last_level and (now - self.last_ts) < COOLDOWN_SEC:
            return
        self.last_level = level
        self.last_ts = now

        try:
            self._publish(n, max_c, level)
        except Exception as e:
            self.get_logger().warn(f"publish failed: {e}")

def main():
    rclpy.init()
    node = ThermalGate()
    try:
        rclpy.spin(node)
    finally:
        try:
            node.mqtt.loop_stop()
            node.mqtt.disconnect()
        except Exception:
            pass
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
