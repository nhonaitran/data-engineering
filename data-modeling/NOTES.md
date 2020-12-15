folder organization

# data modeling
### docker
to run all services in foreground:
```
$ cd ~/data-engineering/data-modeling/docker
$ docker-compose up
```

to run all services in background as daemons:
```
$ docker-compose up -d
```

to stop and remove all containers:
```
$ docker-compose down or
$ docker stop postgres && docker rm postgres
$ docker stop cassandra && docker rm cassandra
```
Notes: 
* the postgres database container is configured to always restart, so you'll see that it'll keep restarting again and again.

* security for postgres database\
create .pgpass file in my home dir to store the database credentials for 
this class

https://tableplus.com/blog/2019/09/how-to-use-pgpass-in-postgresql.html
https://www.postgresql.org/docs/current/libpq-pgpass.html
https://dba.stackexchange.com/questions/14740/how-to-use-psql-with-no-password-prompt


Development workflow would be to use visual studio code to run the jupyter notebooks.  Start the database system contains using the docker-compose file in above docker folder.
Do the above commands to start multiple services at once:
* start postgres:13.1 container
* start cassandra:3.11.9 container

Should continue to add to this docker-compose file to include more services if you want.

Relational databse supports:
* ACID
* 
NoSQL database has simpler design, simpler horizontal scaling, and finer control of availability.


## posgresql

this is a relational database system.
running version 13.1
to login to database system using psql
```
$ psql -h 127.0.0.1 -p 7000 -U postgres -d postgres
Password for user postgres: let'sgo
psql (13.0, server 13.1 (Debian 13.1-1.pgdg100+1))
Type "help" for help.
postgres=#
```


## cassandra

this is one of NoSQL database systems.

### docker

running version 3.11.9

Data structures used are different than those use in relational database; make some operations fast

Basics of cassandra:

* Keyspace
    * Keyspace in Cassandra is much like database in RDBMS world, you can create tables/column families inside keyspace.

* Table
    * a group of partitions

* Partition 
    * fundamental unit of access (similar to schema in relational database)
    * collection of tables
    * partition is how data is distributed


* Rows 

* Primary key
    * partition key + clustering column(s)

* Columns
    * clustering and data columns
    * Labeled element


# Miscellaneous cool tools
http://asciiflow.com/