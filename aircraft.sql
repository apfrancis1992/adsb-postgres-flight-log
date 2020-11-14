CREATE TABLE IF NOT EXISTS
        squitters(
            message_type TEXT,
            transmission_type INT,
            session_id INT,
            aircraft_id INT,
            hex_ident TEXT,
            n_num TEXT,
            flight_id SMALLINT,
            generated_date DATE,
            generated_time TIME,
            logged_date DATE,
            logged_time TIME,
            callsign TEXT,
            altitude INT,
            ground_speed REAL,
            track REAL,
            lat FLOAT8,
            lon FLOAT8,
            vertical_rate SMALLINT,
            distance_nm FLOAT8,
            distance_miles FLOAT8,
            squawk SMALLINT,
            alert SMALLINT,
            emergency SMALLINT,
            spi SMALLINT,
            is_on_ground SMALLINT,
            parsed_time TIMESTAMP
        );

CREATE TABLE IF NOT EXISTS
        flight_log(
            log_id SERIAL PRIMARY KEY,
            n_num_log TEXT,
            pilot_name TEXT,
            start_time TIMESTAMP,
            end_time TIMESTAMP
        );

CREATE TABLE IF NOT EXISTS
        plane_tracker(
            n_num_tracked text PRIMARY KEY,
            active BOOLEAN
        );

CREATE OR REPLACE VIEW callsigns AS
            SELECT callsign, hex_ident, n_num, date(parsed_time) date_seen, max(parsed_time) last_seen, min(parsed_time) first_seen
                FROM squitters
                WHERE callsign != ''
                GROUP BY callsign, hex_ident, n_num, date_seen;


CREATE OR REPLACE VIEW locations AS
            SELECT hex_ident, n_num, parsed_time, lon, lat, altitude, distance_nm
                FROM squitters WHERE lat >= 0;


CREATE OR REPLACE VIEW log_view AS
            SELECT hex_ident, n_num, altitude, ground_speed, track, lat, lon, distance_nm, vertical_rate, squawk, emergency, spi, is_on_ground, generated_date, generated_time, parsed_time
                FROM squitters
                INNER JOIN flight_log
                ON squitters.parsed_time > flight_log.start_time AND squitters.parsed_time < flight_log.end_time AND squitters.n_num = flight_log.n_num_log
                ORDER BY parsed_time;

CREATE OR REPLACE VIEW most_seen AS
            SELECT DISTINCT squitters.n_num,
                count(DISTINCT squitters.generated_date) AS count
                FROM squitters
                GROUP BY squitters.n_num
                ORDER BY (count(DISTINCT squitters.generated_date)) DESC;

CREATE OR REPLACE VIEW tracked_planes AS
            SELECT hex_ident, n_num, altitude, ground_speed, track, lat, lon, distance_nm, vertical_rate, squawk, emergency, spi, is_on_ground, generated_date, generated_time, parsed_time
                FROM squitters
                INNER JOIN plane_tracker
                ON squitters.n_num = plane_tracker.n_num_tracked AND plane_tracker.active = 'yes'
                ORDER BY parsed_time DESC;