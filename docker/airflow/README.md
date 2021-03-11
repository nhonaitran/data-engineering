# Running Airflow Locally in Docker

You can spin up an development/test environment for airflow and dependent
components with docker. You can easily do that by running the commands
`make all && make run` 

Common operations for building image, initialize airflow metadata database
and create user account, start up container, and clean up entire environment
are shown as below.

Currently, the dags, logs, and plugins directories for airflow are configured
to be at ~/workspaces/airflow. A shell script file is provided to map folders
setup for specific projects. Run the script as follows:
```
$ map_airflow_workspace target_dir_full_path source_dir_full_apth
```

## Operations
All of the following operations assume you're already at the root dir:
```
$ cd docker/airflow
```

Use `build` make target to build a new airflow image.  
Make sure the .env file is updated with correct information before proceeding
with this step:
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
