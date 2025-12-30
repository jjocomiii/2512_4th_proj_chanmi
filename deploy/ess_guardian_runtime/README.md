# ESS Guardian Runtime (systemd / udev / /opt layout)

## 포함 내용
- systemd unit: `systemd/etc/systemd/system/ess-*.service`, `ess.target`
- udev rules: `udev/etc/udev/rules.d/99-ess-*.rules`
- /opt 배치 예시: `opt/opt/ess-guardian/current/...`
- python deps: `opt/opt/ess-guardian/current/thermal/requirements.txt`

## 설치(대상 장비에서)
```bash
# systemd
sudo rsync -a systemd/etc/systemd/system/ /etc/systemd/system/
sudo systemctl daemon-reload

# udev
sudo rsync -a udev/etc/udev/rules.d/ /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger

# /opt (필요 파일만)
sudo rsync -a opt/opt/ /opt/
```
활성화 예시
sudo systemctl enable --now ess.target
sudo systemctl enable --now ess-env-daemon.service
sudo systemctl enable --now ess-thermal.service
sudo systemctl enable --now ess-thermal-gate.service


thermal-gate는 ROS 환경(/opt/ros/humble/setup.bash)이 필요할 수 있음.
