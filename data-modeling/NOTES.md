folder organization

#data modeling
Relational databse supports:
* ACID
* 
NoSQL database has simpler design, simpler horizontal scaling, and finer control of availability.


## posgresql

this is a relational database system

## cassandra

this is a NoSQL database system

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

