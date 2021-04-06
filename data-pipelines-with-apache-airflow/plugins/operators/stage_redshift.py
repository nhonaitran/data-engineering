from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import SqlQueries


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 aws_credentials_id,
                 region_name,
                 s3_path,
                 table_name,
                 json_format,
                 *args,
                 **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id,
        self.region_name = region_name,
        self.s3_path = s3_path,
        self.table_name = table_name
        self.json_format = json_format

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info(f"Clearing staging table {self.table_name} in Redshift")
        redshift.run(SqlQueries.clear_table.format(self.table_name))

        aws_hook = AwsHook(aws_conn_id="aws_credentials",
                           region_name=self.region_name,
                           client_type="s3")

        self.log.info("Copying data from S3 to staging table in Redshift")
        credentials = aws_hook.get_credentials(self.region_name)
        copy_data_sql = SqlQueries.copy_sql.format(self.table_name,
                                                   self.s3_path[0],
                                                   credentials.access_key,
                                                   credentials.secret_key,
                                                   self.json_format)
        redshift.run(copy_data_sql)





