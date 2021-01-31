#!/usr/bin/ sh
#
# This shell script extract artist, song, user data from the imported json files.
# Once importing completes, it runs multiple queries to check for ETL results.
#
# Usage:
# sh extract.sh
#

HOST=127.0.0.1
PORT=5432
DATABASE="sparkifydb"
USER="student"

echo "---- perform ETL operations to extract relevant song/artist/user/songs play data"
psql -h $HOST -p $PORT -U $USER -d $DATABASE -f ../sql/etl.sql

echo "---- verify ETL results"
psql -h $HOST -p $PORT -U $USER -d $DATABASE -f ../sql/verify_queries.sql

