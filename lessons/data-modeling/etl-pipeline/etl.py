"""
ETL workflow module for transfering song and log datasets into the 
PostgreSQL database for song play analysis.
"""

import argparse
import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Load given json file into dataframe, extract song and artist data from dataframe and
    insert into songs and artists tables, respectively. 
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 
                    'title', 
                    'artist_id', 
                    'year', 
                    'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = artist_data = df[['artist_id', 
                                    'artist_name', 
                                    'artist_location', 
                                    'artist_latitude', 
                                    'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - Load given json file into dataframe, extract data about the listening session and insert into fact table.
    - Perform looking of user id, song id and artist id for the user.
    - Also breakdown song listening timestamp into much high granular details for analysis
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'])
    
    # insert time data records
    time_data = {
        'ts': df['ts'].values,
        'hour': t.dt.hour,
        'day': t.dt.day,
        'weekofyear': t.dt.isocalendar().week,
        'month': t.dt.month, 
        'year': t.dt.year, 
        'weekday': t.dt.weekday
    }
    column_labels = ('ts', 'hour', 'day', 'weekofyear', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row.values))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        # TODO: better to filter this in the user_df, like anything with userId != ''
        if row.userId == '':
            continue
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        if row.userId == '':
            userId = None
        else:
            userId = row.userId
            
        # TODO: can't figure out how to pass in float value without having convert to string
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, str(row.length)))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.ts,
                        userId,
                        row.level, 
                        songid, 
                        artistid, 
                        row.sessionId,
                        row.location,
                        row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
    """
    Given the database connection and cursor objects, the file path where the data files reside,
    and the function object, this proc traverses the given directory and invoke the given function
    to perform ETL operation on each file found.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    App entry function to kick off the ETL process for given file location
    Initiate the database connection and cursor objects to connect to the 
    PostgreSQL database for data import.
    """
    app_parser = argparse.ArgumentParser(description='Import data from json files into database')
    app_parser.add_argument('Path',
                       metavar='path',
                       type=str,
                       help='the path to json files')
    args = app_parser.parse_args()
    if not os.path.isdir(args.Path):
        print('The path specified does not exist')
        sys.exit()

    conn = None
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
        cur = conn.cursor()

        process_data(cur, conn, filepath=f"{args.Path}/data/song_data", func=process_song_file)
        process_data(cur, conn, filepath=f"{args.Path}/data/log_data", func=process_log_file)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        

if __name__ == "__main__":
    main()