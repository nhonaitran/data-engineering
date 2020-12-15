#!/usr/bin/ sh
#
# This shell script bulk import data from found json files into the given table
# in postgresql database.
# Prior to perform bulk copying, the script truncates the given table first to
# clear out all existing entries.
# 
# Usage:
# sh bulk_import.sh path table_name
#
# Examples: 
# import all json files found under data/log_data directory into table log_data
# sh bulk_import.sh ../data/log_data log_table
#
# import all json files found under data/song_data directory into table song_data
# sh bulk_import.sh ../data/song_data song_table
#
path=$1
table_name=$2

HOST=127.0.0.1
PORT=5432
DATABASE="sparkifydb"
USER="student"

echo "---- setup temp table '${table_name}'..."
psql -h $HOST -p $PORT -U $USER -d $DATABASE -f ../sql/intermediate_tables.sql

echo "---- truncating table '${table_name}'..."
psql -h $HOST -p $PORT -U $USER -d $DATABASE -c "TRUNCATE TABLE ${table_name}"

echo "---- bulk importing data from json files in '${path}' directory into table '${table_name}'..."
for f in $(find $path -maxdepth 5 -name "*.json")
do
    echo $f
    cat $f | sed 's/\\"//g' | psql -h $HOST -p $PORT -U $USER -d $DATABASE -c "COPY ${table_name} (data) FROM STDIN;"
done

echo "---- total count for table '${table_name}'"
psql -h $HOST -p $PORT -U $USER -d $DATABASE -c "SELECT COUNT(*) FROM ${table_name}"
