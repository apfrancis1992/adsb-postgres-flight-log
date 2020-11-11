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

Copyright 2020 apfrancis1992

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.