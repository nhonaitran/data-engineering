.PHONY: venv-create pip-install jupyter-server clean notebook

venv-create:
	python -m venv venv

pip-install: 
	. venv/bin/activate && python -m pip install --upgrade pip && pip install wheel && pip install -r requirements.txt

jupyter-server:
	. venv/bin/activate && jupyter lab

clean:
	rm -rf venv

notebook: venv-create pip-install jupyter-server
