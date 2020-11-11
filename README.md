# ADS-B Logger
Takes ADS-B data from a local receiver and copies it to a local postgres DB.

This python script pulls the data from the pi's TCP datastream on port 30003 and processes the data to be commited to a local Postgres database.

## Installation

Clone the repository.
```bash
git clone https://github.com/apfrancis1992/python-adsb-2-postgres.git
```

Install the python dependencies.
```bash
pip3 install psycopg2-binary
```

## Postgres

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


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
