venv:
	python -m venv .venv

activate-venv: venv
	. .venv/bin/activate

setup: venv activate-venv
	pip install wheel && \
	python -m pip install --upgrade pip && \
	pip install -r requirements.txt

launch-cluster:
	python create_tables.py --command launch

remove-cluster:
	python create_tables.py --command delete

create-dwh:
	python create_tables.py --command create

etl:
	python etl.py

verify:
	python verify.py

check-cluster-status:
	python create_tables.py --command status

pause:
	sleep 120

arun: activate-venv launch-cluster pause create-dwh pause etl pause verify

run: launch-cluster pause create-dwh pause etl pause verify

remove: remove-cluster pause check-cluster-status

clean: activate-venv remove-cluster
	deactivate && rm -rf .venv

