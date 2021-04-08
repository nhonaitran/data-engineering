from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from operators import CreateTablesOperator, \
    StageToRedshiftOperator, \
    LoadFactOperator, \
    LoadDimensionOperator, \
    DataQualityOperator

from helpers import SqlQueries, LoadMode

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2021, 4, 6),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
    'catchup': False,
    'schedule_interval': '@hourly'
}

with DAG(
        'udac_example_dag',
        default_args=default_args,
        description='Load and transform data in Redshift with Airflow',
) as dag:

    start_operator = DummyOperator(task_id='Begin_execution', dag=dag)

    create_tables = CreateTablesOperator(
        task_id='Create_tables',
        redshift_conn_id='redshift',
        dag=dag
    )

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Load_events_from_s3_to_redshift',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        region_name="us-west-2",
        s3_bucket='{{ var.json.s3.bucket }}',
        s3_key='{{ var.json.s3.log_key }}/{{ var.json.s3.log_year }}/{{ var.json.s3.log_month }}',
        table_name='staging_events',
        json_format="s3://udacity-dend/log_json_path.json",
        dag=dag
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='load_songs_from_s3_to_redshift',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        region_name="us-west-2",
        s3_bucket='{{ var.json.s3.bucket }}',
        s3_key='{{ var.json.s3.song_key }}',
        table_name='staging_songs',
        json_format="auto",
        dag=dag
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id='redshift',
        load_mode=LoadMode.TRUNCATE,
        clear_table_sql=SqlQueries.clear_table.format("songplays"),
        load_data_sql=SqlQueries.songplay_table_insert,
        dag=dag
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id='redshift',
        load_mode=LoadMode.TRUNCATE,
        clear_table_sql=SqlQueries.clear_table.format("users"),
        load_data_sql=SqlQueries.user_table_insert,
        dag=dag
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id='redshift',
        load_mode=LoadMode.TRUNCATE,
        clear_table_sql=SqlQueries.clear_table.format("songs"),
        load_data_sql=SqlQueries.song_table_insert,
        dag=dag
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id='redshift',
        load_mode=LoadMode.TRUNCATE,
        clear_table_sql=SqlQueries.clear_table.format("artists"),
        load_data_sql=SqlQueries.artist_table_insert,
        dag=dag
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id='redshift',
        load_mode=LoadMode.TRUNCATE,
        clear_table_sql=SqlQueries.clear_table.format("timeplays"),
        load_data_sql=SqlQueries.time_table_insert,
        dag=dag
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id='redshift',
        tables=SqlQueries.verify_tables,
        dag=dag
    )

    end_operator = DummyOperator(task_id='Stop_execution', dag=dag)

    start_operator >> create_tables >> [stage_events_to_redshift,
                                        stage_songs_to_redshift] >> load_songplays_table

    load_songplays_table >> [load_user_dimension_table,
                             load_song_dimension_table,
                             load_artist_dimension_table,
                             load_time_dimension_table] >> run_quality_checks

    run_quality_checks >> end_operator
