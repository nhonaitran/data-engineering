setup-venv:
	python -m venv .venv

install:
	. .venv/bin/activate && python -m pip install --upgrade pip && pip install wheel && pip install -r requirements.txt

notebook:
	. .venv/bin/activate && jupyter-lab

run: setup-venv install notebook

clean:
	rm -rf .venv



	