# ADS-B Logger
Takes ADS-B data from a local receiver and copies it to a local postgres DB.

This python script pulls the data from the pi's TCP datastream on port 30003 and processes the data to be commited to a local Postgres database.

## PostgreSQL Preparation

SSH to your postgres instance to create a user and database for the program to use.
```bash
ssh username@IP
sudo apt-get install postgresql
psql -d postgres
```

```
CREATE USER username WITH PASSWORD 'password'; 
ALTER USER username WITH SUPERUSER;
CREATE DATABASE aircraft;
EXIT;
```


## Installation

Clone the repository.
```bash
git clone https://github.com/apfrancis1992/adsb-postgres-flight-log.git /opt/adsb-postgres-flight-log
```

Navigate to the root directory and create your configuration file.
```bash
nano /opt/adsb-postgres-flight-log/config.py
```

Enter the following credentials and info
```bash
username = "username" # Postgres DB Username
password = "password" # Postgres DB Password
lat = "xx.xxxx" # ADS-B latitude
lon = "-xx.xxxx" # ADS-B longitude
```

Install the python dependencies.
```bash
pip3 install -r /opt/adsb-postgres-flight-log/requirements.txt
```

Create a Systemd start file
```bash
sudo nano /etc/systemd/system/adsb.service
```

Enter the following config info
```bash
[Unit]
Description=ADS-B Data Capture
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=username
ExecStart=/usr/bin/python3 /opt/adsb-postgres-flight-log/adsb.py

[Install]
WantedBy=multi-user.target
```

Create a log file for the program
```bash
sudo touch /var/log/adsb.log
sudo chown username:username /var/log/adsb.log
```

## ToDo
1. Create tail number tracking to record certain tail numbers.
2. Create a web frontend to view the contents of the database on a map.

## Credit
[@guillaumemichel](https://github.com/guillaumemichel) for his [ICAO – N-Number Converter](https://github.com/guillaumemichel/icao-nnumber_converter).<br/>
[@yanofsky](https://github.com/yanofsky) for his [dump1090 stream parser](https://github.com/yanofsky/dump1090-stream-parser).


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

Copyright 2020 apfrancis1992

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.