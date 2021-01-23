import click
import aws
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Laod data to staging tables
    :param cur: database cursor object
    :param conn: database connection object
    :return: None
    """
    aws.logging.info("Loading data into staging tables")
    for query in copy_table_queries:
        aws.logging.info(f"Executing query \n {query}")
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Load data into fact and dimension tables
    :param cur: database cursor object
    :param conn: database connection object
    :return: None
    """
    aws.logging.info("Loading data into fact and dimension tables")
    for query in insert_table_queries:
        aws.logging.info(f"Executing query \n {query}")
        cur.execute(query)
        conn.commit()


@click.command()
@click.option('--command', default="lst", help='Operation to execute.')
@click.option('--log_level', default="INFO", help='Level of logging.')
def main(command, log_level):
    aws.logging.basicConfig(level=log_level)

    aws.show_cluster_property()

    conn, cur = aws.connect_to_data_warehouse()

    if command == "lst":
        load_staging_tables(cur, conn)
    else:
        insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
