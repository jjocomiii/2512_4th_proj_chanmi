import json
import time
import paho.mqtt.client as mqtt
from db_service import (
    save_environment,
    save_alert,
    get_admin_by_id,
    log_access_result
)

BROKER = "10.10.14.109"
PORT = 1883
RECONNECT_DELAY = 5

# ================================
# MQTT Connect / Subscribe
# ================================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected successfully")
        client.subscribe("ess/env")
        client.subscribe("ess/alert")
        client.subscribe("ess/access/request")
        print("[MQTT] Subscribed: ess/env, ess/alert, ess/access/request")
    else:
        print(f"[MQTT ERROR] Connection failed with code {rc}")


# ================================
# MQTT Message Handler
# ================================
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON: {payload}")
        return

    print(f"[MQTT] Received ({topic}): {data}")

    if topic == "ess/env":
        handle_environment(data)
    elif topic == "ess/alert":
        handle_alert(data)
    elif topic == "ess/access/request":
        handle_access_request(client, data)


# ================================
# Environment / Alert Handlers
# ================================
def handle_environment(data):
    # STM32 발행 JSON: {"t": 23.1, "h": 55.3}
    temp = data.get("t")
    humid = data.get("h")
    save_environment({"temperature": temp, "humidity": humid})


def handle_alert(data):
    save_alert(data)


# ================================
# Access Request Handler
# ================================
def handle_access_request(client, data):
    admin_id = data.get("admin_id")
    access_point = data.get("access_point")

    if not admin_id or not access_point:
        print("[ACCESS ERROR] Missing admin_id or access_point")
        return

    # DB에서 admin 정보 가져오기
    admin = get_admin_by_id(admin_id)

    if admin:
        # admin은admin은 {"id": 3, "access_points": "main,ew2"} 구조라고 가정
        access_points = admin["access_points"]
        allowed_points = [x.strip() for x in access_points.split(",")]

        result = "success" if access_point in allowed_points else "fail"
    else:
        result = "fail"

    # DB 로그 기록
    log_access_result(admin_id=admin_id, access_point=access_point, result=result)

    # STM32로 성공/실패만 응답
    response = {"result": result}
    client.publish("ess/access/response", json.dumps(response))
    print("[ACCESS] response:", response)


# ================================
# Subscriber 실행
# ================================
def run_subscriber():
    while True:
        try:
            client = mqtt.Client(protocol=mqtt.MQTTv311)
            client.on_connect = on_connect
            client.on_message = on_message
            client.connect(BROKER, PORT)
            print("[MQTT] Subscriber started. Waiting for messages...")
            client.loop_forever()
        except Exception as e:
            print(f"[MQTT ERROR] Connection lost: {e}")
            print(f"[MQTT] Reconnecting in {RECONNECT_DELAY} seconds...")
            time.sleep(RECONNECT_DELAY)


# ================================
# Entry Point
# ================================
if __name__ == "__main__":
    run_subscriber()

