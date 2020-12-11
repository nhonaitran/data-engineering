# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS appuser"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS timeplay"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay (songplay_id serial PRIMARY KEY, 
                                    start_time  int, 
                                    user_id     int NOT NULL, 
                                    level       smallint, 
                                    song_id     int NOT NULL, 
                                    artist_id   int NOT NULL, 
                                    session_id  int, 
                                    location    varchar, 
                                    user_agent  varchar);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS appuser (user_id     serial PRIMARY KEY, 
                                    first_name  varchar NOT NULL, 
                                    last_name   varchar NOT NULL, 
                                    gender      varchar, 
                                    level       varchar);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS song (song_id    serial PRIMARY KEY, 
                                title       varchar NOT NULL, 
                                artist_id   int NOT NULL, 
                                year        int, 
                                duration    real);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artist (artist_id    serial PRIMARY KEY, 
                                    name        varchar NOT NULL, 
                                    location    varchar, 
                                    latitude    real, 
                                    longitude   real);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS timeplay (start_time     int, 
                                    hour            smallint, 
                                    day             smallint, 
                                    week            smallint, 
                                    month           smallint, 
                                    year            int, 
                                    weekday         varchar);
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]