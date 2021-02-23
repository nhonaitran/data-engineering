venv:
	@echo + Initiating virtual environment...
	python -m venv .venv

activate-venv:
	@echo + Activating venv...
	. .venv/bin/activate

setup: venv activate-venv
	@echo + Installing dependencies...
	pip install wheel && \
	python -m pip install --upgrade pip && \
	pip install -r requirements.txt

etl:
	@echo + Runnning ETL to extract data from S3...
	python etl.py

clean:
	@echo + Removing the virtual environment...
	rm -rf .venv

run: activate-venv etl

all: setup etl