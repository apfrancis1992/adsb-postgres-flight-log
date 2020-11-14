import socket
import datetime
import time
import psycopg2
import logging
import config
import os
from icao import icao_to_n
from haversine import haversine, Unit

#ADS-B Settings
HOST = "10.0.0.229"
PORT = 30003
BUFFER_SIZE = 1024
BATCH_SIZE = 1
CONNECT_ATTEMPT_LIMIT = 10
CONNECT_ATTEMPT_DELAY = 5.0

#PostgreSQL Settings
host = '127.0.0.1'
port = '5432'
dbname = 'aircraft'
user = config.username
password = config.password

#Logging
log = "/var/log/adsb.log"
cwd = os.getcwd()
sql = cwd
def main():

    # print args.accumulate(args.in)
    count_since_commit = 0
    count_total = 0
    count_failed_connection_attempts = 1

    # connect to database or create if it doesn't exist
    conn = psycopg2.connect(host = host, database = dbname, user = user, password = password)
    cur = conn.cursor()

    # logging
    logging.basicConfig(filename=log, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')

    # set up the table if neccassary
# Open and read the file as a single buffer
    fd = open(os.path.join(cwd, 'aircraft.sql'), 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cur.execute(command)
        except psycopg2.ProgrammingError:
            logging.error("Error running SQL command")


    # open a socket connection
    while count_failed_connection_attempts < CONNECT_ATTEMPT_LIMIT:
        try:
            s = connect_to_socket(HOST, PORT)
            count_failed_connection_attempts = 1
            logging.info("Connected to dump1090 broadcast")
            break
        except socket.error:
            count_failed_connection_attempts += 1
            logging.error("Cannot connect to dump1090 broadcast. Making attempt %s." % (count_failed_connection_attempts))
            time.sleep(CONNECT_ATTEMPT_DELAY)
    else:
        quit()

    data_str = ""

    try:
        #loop until an exception
        while True:
            #get current time
            cur_time = datetime.datetime.utcnow()
            ds = cur_time.isoformat()

            # receive a stream message
            try:
                message = ""
                message = s.recv(BUFFER_SIZE)
                message = message.decode('utf-8')
                data_str = message.strip("\n")
            except socket.error:
                # this happens if there is no connection and is delt with below
                pass

            if len(message) == 0:
                logging.warning("No broadcast received. Attempting to reconnect")
                time.sleep(CONNECT_ATTEMPT_DELAY)
                s.close()

                while count_failed_connection_attempts < CONNECT_ATTEMPT_LIMIT:
                    try:
                        s = connect_to_socket(HOST, PORT)
                        count_failed_connection_attempts = 1
                        logging.info("Reconnected")
                        break
                    except socket.error:
                        count_failed_connection_attempts += 1
                        logging.warning("Reconnection attempt failed. Making attempt %s." % (count_failed_connection_attempts))
                        time.sleep(CONNECT_ATTEMPT_DELAY)
                else:
                    quit()

                continue

            # it is possible that more than one line has been received
            # so split it then loop through the parts and validate
            data = data_str.split("\n")
            for d in data:
                lines = d.split(",")
                #if the line has 22 items, it's valid
                if len(lines) == 22:
                    line = []
                    for r in lines:
                        lines = r.replace('\r', '')
                        line.append(lines)
                    # add the current time to the row
                    line.append(ds)
                    try:
                        line.append(icao_to_n(line[4]))
                    except:
                        line.append(None)
                    try:
                        if line[0] != 'MSG':
                            line[0] = 'MSG'
                        # add the row to the db
                        if not line[5] == '':
                            line[5] = int(line[5])
                        else:
                            line[5] = None
                        if not line[11] == '':
                            line[11] = int(line[11])
                        else:
                            line[11] = None
                        if not line[12] == '':
                            line[12] = float(line[12])
                        else:
                            line[12] = None
                        if not line[13] == '':
                            line[13] = float(line[13])
                        else:
                            line[13] = None
                        if not line[14] == '':
                            line[14] = float(line[14])
                        else:
                            line[14] = None
                        if not line[15] == '':
                            line[15] = float(line[15])
                        else:
                            line[15] = None
                        if not line[16] == '':
                            line[16] = float(line[16])
                        else:
                            line[16] = None
                        if not line[17] == '':
                            line[17] = int(line[17])
                        else:
                            line[17] = None
                        if not line[18] == '':
                            line[18] = int(line[18])
                        else:
                            line[18] = None
                        if not line[19] == '':
                            line[19] = int(line[19])
                        else:
                            line[19] = None
                        if not line[20] == '':
                            line[20] = int(line[20])
                        else:
                            line[20] = None
                        if not line[21] == '':
                            line[21] = int(line[21])
                        else:
                            line[21] = None
                        if line[14] != None:
                            adsb = (float(config.lat), float(config.lon))
                            plane = (line[14], line[15])
                            nm = haversine(adsb, plane, unit=Unit.NAUTICAL_MILES)
                            miles = haversine(adsb, plane, unit=Unit.MILES)
                        else:
                            nm = None
                            miles = None
                        line.append(nm)
                        line.append(miles)
                        cur.executemany("INSERT INTO squitters (message_type,transmission_type,session_id,aircraft_id,hex_ident,flight_id,generated_date,generated_time,logged_date,logged_time,callsign,altitude,ground_speed,track,lat,lon,vertical_rate,squawk,alert,emergency,spi,is_on_ground,parsed_time,n_num,distance_nm,distance_miles) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (line,))

                        # increment counts
                        count_total += 1
                        count_since_commit += 1

                        # commit the new rows to the database in batches
                        if count_since_commit % BATCH_SIZE == 0:
                            conn.commit()
                            count_since_commit = 0

                    except psycopg2.OperationalError:
                        logging.error("Could not write to database, will try to insert %s rows on next commit" % (count_since_commit + BATCH_SIZE,))

                    except psycopg2.OperationalError:
                        logging.error("Could not write to database, will try to insert %s rows on next commit" % (count_since_commit + BATCH_SIZE,))
                    # since everything was valid we reset the stream message
                    data_str = ""
                else:
                    # the stream message is too short, prepend to the next stream message
                    data_str = d
                    continue

    except KeyboardInterrupt:
        logging.info("Closing connection")
        s.close()

        conn.commit()
        conn.close()
        logging.info("%s squitters added to your database" % (count_total))

    except psycopg2.ProgrammingError:
        logging.error("Error with %s" % line)
        quit()

def connect_to_socket(loc,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((loc, port))
    return s

if __name__ == '__main__':
    main()