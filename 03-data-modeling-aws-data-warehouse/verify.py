import aws
import click
import pandas as pd
from sql_queries import verify_tables


def verify_schema(conn):
    """
    Laod data to staging tables
    :param cur: database cursor object
    :param conn: database connection object
    :return: None
    """
    aws.logging.info("Verify data warehouse fact and dimention tables are populated properly")
    for table in verify_tables:
        query = f"SELECT COUNT(*) as total FROM {table};"
        df = pd.read_sql(query, conn)
        aws.logging.info(f"Table {table}: {df['total'][0]} rows.")


@click.command()
@click.option('--log_level', default="INFO", help='Level of logging.')
def main(log_level):
    aws.logging.basicConfig(level=log_level)

    aws.show_cluster_property()

    conn, _ = aws.connect_to_data_warehouse()

    verify_schema(conn)


if __name__ == "__main__":
    main()
