

HOST=127.0.0.1
DBADMIN=postgres
DB=postgres
DB_SCRIPT_DIR=~/src/data-engineering/data-modeling/project-template

all: clean run setup verify

clean:
	@echo ---- shutting down postgresql container
	DOCKER_BUILDKIT=1 docker-compose down -t 90;

run:
	@echo ---- starting up postgresql container
	DOCKER_BUILDKIT=1 docker-compose up -d;

setup:
	sleep 5
	@echo ---- setup studentdb database and student user
	psql -h $(HOST) -U $(DBADMIN) -d $(DB) -f $(DB_SCRIPT_DIR)/create_db_user.sql	
	sleep 5
	@echo ---- drop and create tables
	python $(DB_SCRIPT_DIR)/create_tables.py	
	@echo ---- insert data
	python $(DB_SCRIPT_DIR)/etl.py

verify:
	@echo ---- login to project database
	psql -h $(HOST) -U student -d sparkifydb

.PHONY: clean run setup verify