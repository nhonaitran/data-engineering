#
# Makefile for data modeling project.
#
# Contains make targets for setting up dockerized postgresql database 
# and testing ETL workflow of the data modeling project.
#

HOST=127.0.0.1
DBADMIN=postgres
DB=postgres
PORT=5432
DB_SCRIPT_DIR=~/src/data-engineering/data-modeling/project-template

all: clean run create-db-users create-tables import-data verify

clean:
	@echo ---- shutting down postgresql container
	DOCKER_BUILDKIT=1 docker-compose down -t 90;

run:
	@echo ---- starting up postgresql container
	DOCKER_BUILDKIT=1 docker-compose up -d;

create-db-users:
	sleep 5
	@echo ---- setup studentdb database and student user
	psql -h $(HOST) -p $(PORT) -U $(DBADMIN) -d $(DB) -f $(DB_SCRIPT_DIR)/sql/create_db_user.sql

create-tables:
	sleep 5
	@echo ---- drop and create tables
	python $(DB_SCRIPT_DIR)/create_tables.py

import-data:	
	@echo ---- insert data
	python $(DB_SCRIPT_DIR)/etl.py $(DB_SCRIPT_DIR)

verify:
	@echo ---- verify imported data
	psql -h $(HOST) -p $(PORT) -U student -d sparkifydb -f $(DB_SCRIPT_DIR)/sql/queries.sql
	
.PHONY: clean run setup verify