# Scotty - Sparkify ETL Data Warehouse Pipelines Automation

Scotty is a service that automates Sparkify data warehouse ETL pipelines using Apache Airflow.  Scotty runs the entire ETL workflow every month, and saves the final schema in AWS Redshift for user listening analysis

Scotty is written in Python, and is essentially a complex DAG designed to perform the following the data warehouse pipelines:
* Extract the songs and events datasets from AWS S3 and stage the data in staging tables,
* Create and fill the data warehouse star schema:
  * Create and load the songsplay_fact table,
  * Create and load the song_dim, user_dim, artist_dim, and time_tim dimension tables 
* Perform data validation by running checks on the imported data.

Figure 1. Sparkify data warehouse ETL pipeline
![warehouse-etl-pipeline-dag](../assets/sparkify-etl-pipelines-dag.png)

The log and song datasets are stored S3.  Here is their linksL
* Log data: s3://udacity-dend/log_data
* Song data: s3://udacity-dend/song_data

### Running Scotty in Docker for Development Locally
Go to [running airflow in docker](https://github.com/nhonaitran/data-engineering/tree/master/docker/airflow) for step-by-step instructions on how to setup and run Airflow:v2.0.1rc in docker for development.

Once all the components are up and running, open http://localhost:8080 in Google Chrome for Airflow web UI.  Search for `sparkify-dwh-etl-dag` dag and enable it to begin the pipeline.  