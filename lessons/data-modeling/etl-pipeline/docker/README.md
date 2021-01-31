## docker
shut down running container:
```
make clean
```

start up a container:
```
make run
```

create student user and default:
```
make create-db-users
```

create tables:
```
make create-tables
```

run etl module to import data:
```
make import-data
```

execute queries to verify data imported into database:
```
make verify
```

do all of above operations:
```
make all
```