folder organization

# data modeling
### docker
$ cd ~/data-engineering/data-modeling/docker
$ docker-compose up

Do the above commands to start multiple services at once:
* start a jupyter notebook container
* start a cassandra container as well

Should continue to add to this docker-compose file to include more services if you want.

Relational databse supports:
* ACID
* 
NoSQL database has simpler design, simpler horizontal scaling, and finer control of availability.


## posgresql

this is a relational database system

## cassandra

this is one of NoSQL database systems.

### docker
use following commands to start up the dockerized cassandra instance(s)
$ cd ~/src/data-engineering/data-modeling/cassandra/docker
$ docker-compose up or $ docker-compose up -d


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

