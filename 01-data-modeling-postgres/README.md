# Data Modeling with Postgres

We are going to build the Music relational database in Postgresql to store the
song and user activity collected by the streaming data.

The optimal schema for querying the songs data and user activity is the star schema.
 
## Star Schema for Music Database

To facility song play analysis, the music PostgreSQL database based on a star 
schema is created to store the imported song and log data.

The database schema includes the `songplays` fact table and four dimension tables 
that are linked by the primary keys defined in the dimenion tables.

Users' listening sessions data is stored in the `songplays` fact table.  This 
table only contains the primary key for the song, artist, user, and timestamp 
in each entry.  Metadata such as song title or artist's or user's name, etc. 
can be queried by joining the fact table with the respective dimension tables 
using these primary keys.

![star-schema](../assets/star-schema.png)

Below is brief description of the fact and dimentions tables of the star 
schema created that is optimized for queries on song play analysis.

### Fact Table
1. songplays - records in log data associated with song plays.  This table 
contains the session information, with referential key for specific user, 
song played, and the song's artist linked to the `users`, `songs`, `artists`, 
and `time` tables, respectively.

### Dimension Tables
1. users - users captured from log dataset
2. songs - songs in music database
3. artists - artists in music database
5. time - timestamps of records in `songplays` broken down into specific units

Each dimension table has a primary key which is used to join with the 
`songplays` fact table for getting more detail information about the 
song(s), the artist(s), the user(s), and/or relevant time related to 
the listening session.

## ETL Pipeline Workflow

The data ETL workflow uses different technique to import the data dependent 
on the size of the datasets.  Each technique is described below.

### Working with small datasets
A dockerized environment with postgresql database is setup to load music data 
into an independent  music database with ease.  A Makefile is provided in 
the `docker` directory that can use to either run individual commands as needed 
or `make all` to perform the entire ETL pipeline.

This method is suited for importing small datasets into the database. This 
is due to the fact that the ETL python module is written to traverse the log 
and song directories and process the json file by file, which can take a few minutes.

Please refer to the `Working with large datasets` section for faster 
method of importing data using COPY command avaiable in Postgresql.


To run the entire ETL pipeline, at the project root directory `etl-pipeline`, 
type the followings:

Download this repo to local machine, and go to the `data-modeling`
```
$ git clone https://github.com/nhonaitran/data-engineering.git
$ cd data-engineering/data-modeling
```

then project dir, setup virtual environment, install library dependencies, and off we go:
```
$ cd etl-pipeline
$ python -v venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ cd docker
$ make all
```

The `all` make target performs the following tasks:
1. shut down the docker posrgresl (and cassandra) container, and remove it
2. start up a new postgresql container
3. create the student role (with appropriate privileges granted) and default database
4. run the `create_tables` python module to create the tables in the sparkifydb database
5. run the `etl` module with given path where the json files reside
6. run sql scripts to verify data is imported into the table as expected.  

### Working with large datasets
For larger datasets, Postgresql database provides the COPY command that
can be used for fast batch importing data into the database.

A couple of shell scripts are provided for kick off the data import and 
ETL processing with SQL scripts. At the project root directory 
`etl-pipeline`, type the followings:
```
$ cd etl-pipeline/bin
$ sh bulk-import.sh ../data/log_data log_data
$ sh bulk-import.sh ../data/song_data song_data
$ sh extract_and_verify.sh 
```

The `bulk-import` shell script reads in the content of the json files and 
invoke the COPY command provided by Postgresql to import the json content 
the given table name

The `extract_and_verify` shell script then run ETL SQL scripts to extract 
songs, artists, users and songplays data from the holding table into their 
own tables as described in above star schema for the database.