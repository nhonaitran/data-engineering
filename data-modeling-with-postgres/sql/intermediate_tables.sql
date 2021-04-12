-- sql script for creating the staging tables for storing the json files
BEGIN;
CREATE TABLE IF NOT EXISTS log_data (id serial PRIMARY KEY, data jsonb NOT NULL, added timestamp default now());
CREATE TABLE IF NOT EXISTS song_data (id serial PRIMARY KEY, data jsonb NOT NULL, added timestamp default now());
COMMIT;
