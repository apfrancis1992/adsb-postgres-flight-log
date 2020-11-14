#!/bin/bash

systemd=/etc/systemd/system/adsb.service
config=/opt/adsb-postgres-flight-log/config.py

# Create Systemd file
if [ -f "$systemd" ]; then
    echo "Removing existing systemd file."
    rm $systemd
    echo "Creating new systemd file."
else 
    echo "Creating new systemd file."
fi
touch $systemd

# Systemd Config
echo "[Unit]" >> $systemd
echo "Description=ADS-B Data Capture" >> $systemd
echo "After=network.target" >> $systemd
echo "StartLimitIntervalSec=0" >> $systemd
echo -e "\n[Service]" >> $systemd
echo "Type=simple" >> $systemd
echo "Restart=always" >> $systemd
echo "RestartSec=1" >> $systemd
echo "User=$SUDO_USER" >> $systemd
echo "ExecStart=/usr/bin/python3 /opt/adsb-postgres-flight-log/adsb.py" >> $systemd
echo -e "\n[Install]" >> $systemd
echo "WantedBy=multi-user.target" >> $systemd


echo "Enter database password for $SUDO_USER: "
read PASSWORD
read LAT
read LON
echo 'username = "$SUDO_USER"' >> $config
echo 'password = "$PASSWORD"' >> $config
echo 'lat = "$PASSWORD"' >> $config
echo 'lon = "$PASSWORD"' >> $config