TRUNCATE TABLE artists;
TRUNCATE TABLE songs;
TRUNCATE TABLE users;
TRUNCATE TABLE songplays;

-- extract artists from song_data table
INSERT INTO artists
SELECT distinct data->>'artist_id' as artist_id
        , data->>'artist_name' as artist_name
        , data->>'artist_location' as artist_location
        , CASE 
            WHEN data->>'artist_latitude' IS NULL THEN NULL 
            ELSE CAST(data->>'artist_latitude' AS real) 
          END as artist_latitude
        , CASE 
            WHEN data->>'artist_longitude' IS NULL THEN NULL 
            ELSE CAST(data->>'artist_longitude' AS real) 
          END as artist_longitude
FROM song_data
ORDER BY data->>'artist_id';


-- extract songs from song_data table
INSERT INTO songs
SELECT distinct data->>'song_id' as song_id
        , data->>'title' as title
        , data->>'artist_id' as artist_id
        , CASE 
            WHEN data->>'duration' IS NULL THEN NULL 
            ELSE CAST(data->>'duration' AS real) 
          END as duration
        , CASE 
            WHEN data->>'year' IS NULL THEN NULL 
            ELSE CAST(data->>'year' AS int) 
          END as year
FROM song_data
ORDER BY data->>'song_id';

-- extract users from log_data table
INSERT INTO users
SELECT distinct CAST(data->>'userId' AS int) as user_id
        , data->>'firstName' as first_name
        , data->>'lastName' as last_name
        , data->>'gender' as gender
        , data->>'location' as location
FROM log_data
WHERE data->>'userId' != ''
ORDER BY user_id;

-- extract songplays from log_data table
INSERT INTO songplays
SELECT CASE 
            WHEN data->>'sessionId' IS NULL THEN NULL 
            ELSE CAST(data->>'sessionId' AS int) 
          END as session_id
        , data->>'level' as level
        , data->>'ts' as start_time
        , CASE
            WHEN TRIM(data->>'userId') = '' THEN NULL
            ELSE CAST(data->>'userId' as int)
          END as user_id
        , artists.id as artist_id 
        , songs.id as song_id
        , data->>'userAgent' as user_agent
FROM log_data
    LEFT JOIN artists ON log_data.data->>'artist' = artists.name
    LEFT JOIN songs ON artists.id = songs.artist_id and trim(data->>'song') = songs.title
;

