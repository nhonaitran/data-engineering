import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS timeplays"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events (
	
)
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs (
)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
	songplay_id serial PRIMARY KEY,
	start_time	varchar,
	user_id		int NOT NULL,
	level		varchar,
	song_id		varchar,
	artist_id	varchar,
	session_id	int NOT NULL,
	location	varchar,
	user_agent	varchar
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
	user_id 	int PRIMARY KEY,
	first_name	varchar NOT NULL,
	last_name	varchar NOT NULL,
	gender		varchar,
	level		varchar
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
	song_id		varchar PRIMARY KEY,
	title		varchar NOT NULL,
	artist_id	varchar NOT NULL,
	year		int,
	duration	real
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
	artist_id	varchar PRIMARY KEY,
	name		varchar NOT NULL,
	location	varchar,
	latitude	real,
	longitude	real
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
	start_time 	varchar PRIMARY KEY,
	hour		smallint,
	day			smallint,
	week		smallint,
	month		smallint,
	year		int,
	weekday		varchar
);
""")

# STAGING TABLES

staging_events_copy = ("""
	COPY staging_events FROM '{}'
	credentials 'aws_iam_role={}'
	gzip delimiter ';'	
""").format(DWH_DATASET, DWH_ROLE_ARN)

staging_songs_copy = ("""
	COPY staging_songs FROM '{}'
	credentials 'aws_iam_role={}'
	gzip delimiter ';'
""").format(DWH_DATASET, DWH_ROLE_ARN)

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
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users (
    user_id, 
    first_name, 
    last_name, 
    gender, 
    level
) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE 
SET first_name = EXCLUDED.first_name, 
    last_name = EXCLUDED.last_name, 
    gender = EXCLUDED.gender, 
    level = EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs (
    song_id, 
    title, 
    artist_id,
    year, 
    duration
) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artists (
    artist_id, 
    name, 
    location, 
    latitude, 
    longitude
) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
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
) VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
