venv:
	python -m venv .venv

setup: venv
	source .venv/bin/activate && \
	pip install wheel && \
	python -m pip install --upgrade pip && \
	pip install -r requirements.txt

clean:
	source .venv/bin/activate && deactivate && rm -rf .venv