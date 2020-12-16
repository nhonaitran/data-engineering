SELECT COUNT(*) total_songs FROM songs;

SELECT COUNT(*) total_artists FROM artists;

SELECT COUNT(*) total_users FROM users;

SELECT COUNT(*) total_songs_played FROM songplays;

SELECT COUNT(*) = 1 as etl_passed FROM songplays WHERE song_id IS NOT NULL AND artist_id IS NOT NULL;

SELECT sp.songplay_id
        , sp.start_time, t.hour, t.day, t.week, t.month, t.year, t.weekday
        , sp.user_id, u.first_name || ' ' || u.last_name as user_name
        , sp.artist_id, a.name
        , sp.song_id, s.title
        , sp.session_id, sp.location, sp.user_agent 
FROM songplays sp
        left join time t on sp.start_time = t.start_time
        left join users u ON sp.user_id = u.user_id 
        left join artists a on sp.artist_id = a.artist_id 
        left join songs s on sp.song_id = s.song_id
WHERE   sp.song_id IS NOT NULL 
AND     sp.artist_id IS NOT NULL;