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
ORDER BY data->>'artist_id'
ON CONFLICT DO NOTHING;


-- extract songs from song_data table
INSERT INTO songs
SELECT distinct data->>'song_id' as song_id
        , data->>'title' as title
        , data->>'artist_id' as artist_id
        , CASE 
            WHEN data->>'year' IS NULL THEN NULL 
            ELSE CAST(data->>'year' AS int) 
          END as year
        , CASE 
            WHEN data->>'duration' IS NULL THEN NULL 
            ELSE CAST(data->>'duration' AS real) 
          END as duration
FROM song_data
ORDER BY data->>'song_id'
ON CONFLICT DO NOTHING;

-- extract users from log_data table
INSERT INTO users
SELECT distinct CAST(data->>'userId' AS int) as user_id
        , data->>'firstName' as first_name
        , data->>'lastName' as last_name
        , data->>'gender' as gender
        , data->>'level' as level
FROM log_data
WHERE data->>'page' = 'NextSong'
AND   data->>'userId' != ''
ORDER BY user_id
ON CONFLICT (user_id) DO NOTHING;
--DO UPDATE SET (first_name, last_name, gender, level) = (EXCLUDED.first_name, EXCLUDED.last_name, EXCLUDED.gender, EXCLUDED.level);
--TODO: unable to perform upsert on multiple entries here; need to figure out how to go around this issue;

-- extract songplays from log_data table
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT  data->>'ts' as start_time
        , CASE
            WHEN TRIM(data->>'userId') = '' THEN NULL
            ELSE CAST(data->>'userId' as int)
          END as user_id
        , data->>'level' as level
        , songs.song_id
        , artists.artist_id 
        , CASE 
            WHEN data->>'sessionId' IS NULL THEN NULL 
            ELSE CAST(data->>'sessionId' AS int) 
          END as session_id
        , data->>'location'
        , data->>'userAgent' as user_agent
FROM log_data
    LEFT JOIN artists ON log_data.data->>'artist' = artists.name
    LEFT JOIN songs ON artists.artist_id = songs.artist_id and trim(data->>'song') = songs.title
WHERE data->>'page' = 'NextSong';

