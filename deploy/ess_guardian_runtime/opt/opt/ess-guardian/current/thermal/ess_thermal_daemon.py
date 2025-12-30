#!/usr/bin/env python3
import json
import time
import os
from datetime import datetime

import adafruit_mlx90640

OUT = "/var/log/ess-thermal-status.json"

I2C_BUS = int(os.getenv("ESS_THERM_I2C_BUS", "9"))
FPS_HZ = float(os.getenv("ESS_THERM_HZ", "1.0"))          # status 파일 갱신 주기
REFRESH = os.getenv("ESS_THERM_REFRESH", "2HZ")          # MLX 내부 refresh

# ROI: 정가운데 20x7 (32x24 기준)
ROI_W = int(os.getenv("ESS_THERM_ROI_W", "7"))
ROI_H = int(os.getenv("ESS_THERM_ROI_H", "20"))

W, H = 32, 24  # MLX90640 frame size


def now_ts():
    # +0900 포함 포맷
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")


def atomic_write_json(path: str, payload: dict):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f, ensure_ascii=False)
    os.replace(tmp, path)


def open_i2c(bus: int):
    # bus 9 쓰려고 ExtendedI2C 사용
    from adafruit_extended_bus import ExtendedI2C as I2C
    return I2C(bus)


def set_refresh(mlx):
    # 문자열로 받되 안전하게 매핑
    m = {
        "0.5HZ": adafruit_mlx90640.RefreshRate.REFRESH_0_5_HZ,
        "1HZ":   adafruit_mlx90640.RefreshRate.REFRESH_1_HZ,
        "2HZ":   adafruit_mlx90640.RefreshRate.REFRESH_2_HZ,
        "4HZ":   adafruit_mlx90640.RefreshRate.REFRESH_4_HZ,
        "8HZ":   adafruit_mlx90640.RefreshRate.REFRESH_8_HZ,
        "16HZ":  adafruit_mlx90640.RefreshRate.REFRESH_16_HZ,
        "32HZ":  adafruit_mlx90640.RefreshRate.REFRESH_32_HZ,
        "64HZ":  adafruit_mlx90640.RefreshRate.REFRESH_64_HZ,
    }
    key = str(REFRESH).upper()
    mlx.refresh_rate = m.get(key, adafruit_mlx90640.RefreshRate.REFRESH_2_HZ)


def compute_center_roi():
    x0 = max(0, (W - ROI_W) // 2)
    y0 = max(0, (H - ROI_H) // 2)
    # 혹시 환경변수로 이상하게 들어오면 clamp
    x0 = min(x0, W - 1)
    y0 = min(y0, H - 1)
    w = min(ROI_W, W - x0)
    h = min(ROI_H, H - y0)
    return x0, y0, w, h


def roi_min_max(frame, x0, y0, w, h):
    tmin = None
    tmax = None
    max_x = x0
    max_y = y0
    # ROI 내부만 스캔
    for yy in range(y0, y0 + h):
        base = yy * W
        for xx in range(x0, x0 + w):
            v = frame[base + xx]
            if tmin is None or v < tmin:
                tmin = v
            if tmax is None or v > tmax:
                tmax = v
                max_x, max_y = xx, yy
    return float(tmin), float(tmax), max_x, max_y


def main():
    frame = [0.0] * (W * H)
    mlx = None

    while True:
        x0, y0, w, h = compute_center_roi()

        # (1) init/reinit
        if mlx is None:
            try:
                i2c = open_i2c(I2C_BUS)
                mlx = adafruit_mlx90640.MLX90640(i2c)
                set_refresh(mlx)
            except Exception as e:
                atomic_write_json(OUT, {
                    "timestamp": now_ts(),
                    "i2c_bus": I2C_BUS,
                    "roi": {"x0": x0, "y0": y0, "w": w, "h": h},
                    "error": f"init_fail: {repr(e)}",
                })
                time.sleep(1.0)
                continue

        # (2) capture
        try:
            mlx.getFrame(frame)
            tmin, tmax, max_x, max_y = roi_min_max(frame, x0, y0, w, h)

            payload = {
                "timestamp": now_ts(),
                "min_c": tmin,
                "max_c": tmax,
                # 절대좌표(32x24 기준)
                "max_pos": {"x": int(max_x), "y": int(max_y)},
                # ROI 내부좌표(0~w-1, 0~h-1)도 같이 제공
                "max_pos_roi": {"x": int(max_x - x0), "y": int(max_y - y0)},
                "i2c_bus": I2C_BUS,
                "roi": {"x0": x0, "y0": y0, "w": w, "h": h},
            }
            atomic_write_json(OUT, payload)

        except Exception as e:
            atomic_write_json(OUT, {
                "timestamp": now_ts(),
                "i2c_bus": I2C_BUS,
                "roi": {"x0": x0, "y0": y0, "w": w, "h": h},
                "error": f"frame_fail: {repr(e)}",
            })
            # 센서 상태가 꼬였을 수 있으니 re-init 유도
            mlx = None
            time.sleep(0.5)

        time.sleep(max(0.05, 1.0 / FPS_HZ))


if __name__ == "__main__":
    main()
