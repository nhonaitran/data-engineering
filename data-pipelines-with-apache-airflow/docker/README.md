# Running Airflow Locally in Docker

You can spin up a development/test environment for building data pipelines
with Apache Airflow in Docker. You can easily do that by running the commands
`make all && make run` 

Common operations for building image, initialize airflow metadata database
and create user account, start up container, and clean up entire environment
are shown as below.

Currently, the dags, logs, and plugins directories for airflow are configured
to be at ~/src/data-engineering/data-pipeline-with-apache-airflow. 
Update the .env file if you change the path of this directory.

## Operations
Go to the project workspace directory:
```
$ cd ~/src/data-engineering/data-pipeline-with-apache-airflow
$ mkdir ./dags ./logs ./plugins
$ cd docker
```

Update the .env file with appropriate values for your environment, then use `build` make target to build a new airflow image:
```
$ make build
```

Use `init` make target to initialize airflow metadata database and create
user account:
```
$ make init
```

Use `run` make target to start up airflow container and dependent containers:
```
$ make run
```

Use `clean` make target to stop and delete all containers, images, and data
volumes created for airflow:
```
$ make clean
```
