SELECT COUNT(*) total_songs FROM songs;

SELECT COUNT(*) total_artists FROM artists;

SELECT COUNT(*) total_users FROM users;

SELECT COUNT(*) total_songs_played FROM songplays;

SELECT COUNT(*) = 1 as etl_passed FROM songplays WHERE song_id IS NOT NULL AND artist_id IS NOT NULL;