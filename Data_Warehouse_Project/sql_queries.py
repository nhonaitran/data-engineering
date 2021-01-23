import aws

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS timeplays"

# CREATE TABLES

staging_events_table_create = ("""
CREATE TABLE staging_events (
    artist varchar,
    auth varchar,
    firstName varchar,
    gender varchar,
    itemInSession varchar NOT NULL,
    lastName varchar,
    length varchar,
    level varchar,
    location varchar,
    method varchar NOT NULL,
    page varchar,
    registration varchar,
    sessionId varchar,
    song varchar,
    status varchar,
    ts varchar NOT NULL,
    userAgent varchar,
    userId varchar NOT NULL
)
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs (
    song_id varchar NOT NULL,
    num_songs varchar NOT NULL,
    title varchar NOT NULL,
    artist_name varchar NOT NULL, 
    artist_latitude varchar,
    year varchar NOT NULL,
    duration varchar NOT NULL,
    artist_id varchar NOT NULL,
    artist_longitude varchar,
    artist_location varchar
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
songplay_id int IDENTITY(1,1),
start_time	varchar,
user_id		int NOT NULL,
level		varchar,
song_id		varchar,
artist_id	varchar,
session_id	int NOT NULL,
location	varchar,
user_agent	varchar,
PRIMARY KEY(songplay_id)
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
user_id 	int NOT NULL,
first_name	varchar NOT NULL,
last_name	varchar NOT NULL,
gender		varchar,
level		varchar,
PRIMARY KEY(user_id)
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id		varchar,
title		varchar NOT NULL,
artist_id	varchar NOT NULL,
year		int,
duration	real,
PRIMARY KEY(song_id)
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id	varchar,
name		varchar NOT NULL,
location	varchar,
latitude	real,
longitude	real,
PRIMARY KEY(artist_id)
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time 	varchar,
hour		smallint,
day			smallint,
week		smallint,
month		smallint,
year		int,
weekday		varchar,
PRIMARY KEY(start_time)
);
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events 
FROM {}
CREDENTIALS 'aws_iam_role={}'
JSON 's3://udacity-dend/log_json_path.json';
""").format(aws.LOG_DATA, aws.DWH_ROLE_ARN)

staging_songs_copy = ("""
COPY staging_songs 
FROM {}
CREDENTIALS 'aws_iam_role={}'
JSON 'auto';
""").format(aws.SONG_DATA, aws.DWH_ROLE_ARN)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (
    start_time,
    user_id,
    level,
    song_id,
    artist_id,
    session_id,
    location,
    user_agent
)
SELECT se.ts, se.userId::int, se.level, s.song_id, a.artist_id, se.sessionId::int, se.location, se.userAgent
FROM staging_events se 
        LEFT JOIN songs s ON se.song = s.title
        LEFT JOIN artists a ON se.artist = a.name
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level) 
SELECT DISTINCT userId::int, firstName, lastName, gender, level
FROM staging_events
WHERE page = 'NextSong'
AND userId NOT IN (SELECT user_id FROM users);
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT song_id, title, artist_id, year::smallint, duration::real
FROM staging_songs
WHERE song_id NOT IN (SELECT song_id FROM songs);
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT artist_id, artist_name, null, artist_latitude::real, artist_longitude::real
FROM staging_songs
WHERE artist_id NOT IN (SELECT artist_id FROM artists);
""")

time_table_insert = ("""
INSERT INTO time (
    start_time,
    hour,
    day,
    week,
    month,
    year,
    weekday
)
WITH songplay_timestamp AS (
  	SELECT ts, timestamp 'epoch' + cast(ts AS bigint)/1000 * interval '1 second' as timestamp_col
	FROM staging_events
	WHERE page = 'NextSong'
)
SELECT ts,
        extract(hour from timestamp_col) as hour,
        extract(day from timestamp_col) as day,
        extract(week from timestamp_col) as week,
        extract(month from timestamp_col) as month,
        extract(year from timestamp_col) as year,
        extract(weekday from timestamp_col) as weekday
FROM songplay_timestamp;
""")

staging_events_count = ("""
SELECT COUNT(*) as total
FROM staging_events;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create,
                        songplay_table_create,
                        user_table_create,
                        song_table_create,
                        artist_table_create,
                        time_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop,
                      songplay_table_drop,
                      user_table_drop,
                      song_table_drop,
                      artist_table_drop,
                      time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [user_table_insert,
                        time_table_insert,
                        artist_table_insert,
                        song_table_insert,
                        songplay_table_insert]


