import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
	"""
	Drop each table using the queries in 'drop_table_queries' list.
	"""
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
	"""
    Create each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
	# Load data warehouse configuration settings
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

	# connect to the database and get cursor to it
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

	# drop all tables
    drop_tables(cur, conn)

	# create all tables
    create_tables(cur, conn)

	# close connection to database
    conn.close()


if __name__ == "__main__":
    main()