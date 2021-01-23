import click
import logging
import aws
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drop each table using the queries in 'drop_table_queries' list.
    """
    logging.info("Dropping existing tables")
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create each table using the queries in `create_table_queries` list.
    """
    logging.info("Creating tables")
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


@click.command()
@click.option('--command', default="create", help='Operation to execute.')
@click.option('--log_level', default="INFO", help='Level of logging.')
def main(command, log_level):
    # setting program logging
    logging.basicConfig(level=log_level)

    if command == "launch":
        if aws.setup_role():
            aws.create_cluster()
            aws.show_cluster_property()

    elif command == "delete":
        aws.show_cluster_property()
        aws.delete_cluster()

    elif command == "create":
        conn, cur = aws.connect_to_data_warehouse()
        drop_tables(cur, conn)
        create_tables(cur, conn)
        conn.close()
        logging.info("Finish creating tables")

    else:
        aws.show_cluster_property()


if __name__ == "__main__":
    main()
