AUTO START
1. sudo nano /lib/systemd/system/sample.service
2. type:
    [Unit]
    Description=My Sample Service
    After=multi-user.target

    [Service]
    Type=idle
    ExecStart=/usr/bin/python /home/pi/sample.py

    [Install]
    WantedBy=multi-user.target

3. sudo chmod 644 /lib/systemd/system/sample.service
4. sudo systemctl daemon-reload
   sudo systemctl enable sample.service

5.reboot