from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import LoadMode


class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 load_mode,
                 clear_table_sql,
                 load_data_sql,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.loadMode = load_mode
        self.clear_table_sql = clear_table_sql
        self.load_data_sql = load_data_sql

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.loadMode is LoadMode.TRUNCATE:
            self.log.info(f"Clearing table...")
            redshift.run(self.clear_table_sql)

        self.log.info(f"Inserting data...")
        redshift.run(self.load_data_sql)