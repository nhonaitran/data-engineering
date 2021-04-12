.PHONY: buid pull run

build:
	python -m venv venv

pull:
	docker pull cassandra

run:
	docker run --name cassandra --network some-network -d cassandra:tag
