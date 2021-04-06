class SqlQueries:

    # CREATE TABLES

    staging_events_table_create = ("""
        BEGIN;
        DROP TABLE IF EXISTS staging_events;
        CREATE TABLE staging_events (
            artist varchar(256),
            auth varchar(256),
            firstname varchar(256),
            gender varchar(256),
            iteminsession int4,
            lastname varchar(256),
            length numeric(18,0),
            "level" varchar(256),
            location varchar(256),
            "method" varchar(256),
            page varchar(256),
            registration numeric(18,0),
            sessionid int4,
            song varchar(256),
            status int4,
            ts int8,
            useragent varchar(256),
            userid int4
        );
        COMMIT;
    """)

    staging_songs_table_create = ("""
        BEGIN;
        DROP TABLE IF EXISTS staging_songs;
        CREATE TABLE staging_songs (
            num_songs int4,
            artist_id varchar(256),
            artist_name varchar(256),
            artist_latitude numeric(18,0),
            artist_longitude numeric(18,0),
            artist_location varchar(256),
            song_id varchar(256),
            title varchar(256),
            duration numeric(18,0),
            "year" int4
        );
        COMMIT;
    """)

    songplay_table_create = ("""
        BEGIN;
        DROP TABLE IF EXISTS songplays;
        CREATE TABLE IF NOT EXISTS songplays (
            playid varchar(32) NOT NULL,
            start_time timestamp NOT NULL,
            userid int4 NOT NULL,
            "level" varchar(256),
            songid varchar(256),
            artistid varchar(256),
            sessionid int4,
            location varchar(256),
            user_agent varchar(256),
            CONSTRAINT songplays_pkey PRIMARY KEY (playid)
        );
        COMMIT;
    """)

    user_table_create = ("""
        BEGIN;
        DROP TABLE IF EXISTS users;
        CREATE TABLE IF NOT EXISTS users (
            userid int4 NOT NULL,
            first_name varchar(256),
            last_name varchar(256),
            gender varchar(256),
            "level" varchar(256),
            CONSTRAINT users_pkey PRIMARY KEY (userid)
        );
        COMMIT;
    """)

    song_table_create = ("""
        BEGIN;
        DROP TABLE IF EXISTS songs;
        CREATE TABLE IF NOT EXISTS songs (
            songid varchar(256) NOT NULL,
            title varchar(256),
            artistid varchar(256),
            "year" int4,
            duration numeric(18,0),
            CONSTRAINT songs_pkey PRIMARY KEY (songid)
        );
        COMMIT;
    """)

    artist_table_create = ("""
        BEGIN;
        DROP TABLE IF EXISTS artists;
        CREATE TABLE IF NOT EXISTS artists (
            artistid varchar(256) NOT NULL,
            name varchar(256),
            location varchar(256),
            latitude numeric(18,0),
            longitude numeric(18,0)
        );
        COMMIT;
    """)

    time_table_create = ("""
        BEGIN;
        DROP TABLE IF EXISTS timeplays;
        CREATE TABLE IF NOT EXISTS timeplays (
            start_time timestamp NOT NULL,
            "hour" int4,
            "day" int4,
            week int4,
            "month" varchar(256),
            "year" int4,
            weekday varchar(256),
            CONSTRAINT time_pkey PRIMARY KEY (start_time)
        );
        COMMIT;
    """)

    # STAGING TABLES

    copy_sql = ("""
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        JSON '{}';
    """)

    # FINAL TABLES
    songplay_table_insert = ("""
        BEGIN; 
        INSERT INTO songplays (
            playid,
            start_time,
            userid,
            level,
            songid,
            artistid,
            sessionid,
            location,
            user_agent
        )
        SELECT
                md5(events.sessionid || events.start_time) songplay_id,
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id, 
                songs.artist_id, 
                events.sessionid, 
                events.location, 
                events.useragent
                FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration;
        COMMIT;
    """)

    user_table_insert = ("""
        BEGIN; 
        INSERT INTO users (userid, first_name, last_name, gender, level)
        SELECT DISTINCT userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page = 'NextSong'
        AND userid NOT IN (SELECT userid FROM users)
        ;
        COMMIT;
    """)

    song_table_insert = ("""
        BEGIN; 
        INSERT INTO songs (songid, title, artistid, year, duration)
        SELECT DISTINCT song_id, title, artist_id, year, duration
        FROM staging_songs
        WHERE song_id NOT IN (SELECT songid FROM songs);
        COMMIT;
    """)

    artist_table_insert = ("""
        BEGIN; 
        INSERT INTO artists (artistid, name, location, latitude, longitude)
        SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
        WHERE artist_id NOT IN (SELECT artistid FROM artists);
        COMMIT;
    """)

    time_table_insert = ("""
        BEGIN; 
        INSERT INTO timeplays (start_time, hour, day, week, month, year, weekday)
        SELECT start_time, 
                extract(hour from start_time), 
                extract(day from start_time), 
                extract(week from start_time), 
                extract(month from start_time), 
                extract(year from start_time), 
                extract(dayofweek from start_time)
        FROM songplays;
        COMMIT;
    """)

    clear_table = ("""
        BEGIN; 
        DELETE FROM {}; 
        COMMIT;
    """)

    rows_count = ("""
        SELECT count(*)
        FROM {};
    """)

    # QUERY LISTS

    create_table_queries = [staging_events_table_create,
                            staging_songs_table_create,
                            songplay_table_create,
                            user_table_create,
                            song_table_create,
                            artist_table_create,
                            time_table_create]

    insert_table_queries = [user_table_insert,
                            time_table_insert,
                            artist_table_insert,
                            song_table_insert,
                            songplay_table_insert]

    verify_tables = ["staging_events", "staging_songs", "users", "timeplays", "artists", "songs", "songplays"]

