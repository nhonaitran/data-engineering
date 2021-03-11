APP_VERSION ?= 2.0.1rc
DOCKER_IMAGE_NAME = apache/airflow

all: build init

init:
	@echo Starting to run database migrations and create the first user account, which has the login airflow and the password airflow
	docker-compose up airflow-init

build:
	@echo Building images for airflow and dependent services
	docker build --no-cache . -t $(DOCKER_IMAGE_NAME):$(APP_VERSION)

run:
	@echo Starting all services
	docker-compose up -d

clean:
	@echo Stopping containers: delete containers, volumes with database data, and images
	docker-compose down --volumes --rmi all

.PHONY: build clean init run