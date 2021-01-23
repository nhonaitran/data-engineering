venv:
	@echo Initiating virtual environment...
	python -m venv .venv

activate-venv: venv
	@echo Activating venv...
	. .venv/bin/activate

setup: venv activate-venv
	@echo Installing dependencies...
	pip install wheel && \
	python -m pip install --upgrade pip && \
	pip install -r requirements.txt

launch-cluster:
	@echo Launching cluster...
	python create_tables.py --command launch

remove-cluster:
	@echo Removing cluster...
	python create_tables.py --command delete

create-dwh:
	@echo Creating data warehouse schema...
	python create_tables.py --command create

etl:
	@echo Runnning ETL to populate data warehouse schema...
	python etl.py

verify:
	@echo Verifying the total count of all fact and dimension tables...
	python verify.py

check-cluster-status:
	@echo Checking cluster current status...
	python create_tables.py --command status

pause:
	sleep 120

arun: setup launch-cluster pause create-dwh pause etl pause verify

run: launch-cluster pause create-dwh pause etl pause verify

remove: remove-cluster pause check-cluster-status

clean: remove-cluster pause
	rm -rf .venv

