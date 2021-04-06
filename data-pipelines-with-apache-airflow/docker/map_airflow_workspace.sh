#!/usr/env/bin bash
#
# This maps the dags, logs, and plugins folders for airflow to 
# another specific folders.  The default airflow directory is ~/workspaces/airflow
#
# Examples:
# ./map_airflow_workspaces.sh ~/src/data-engineering/lessons/data-pipeline-with-airflow/exercises
# ./map_airflow_workspaces.sh ~/src/data-engineering/lessons/data-pipeline-with-airflow/exercises ~/workspaces/airflow

TARGET_DIR=$1
SOURCE_DIR=$2

ln -s $(SOURCE_DIR)/dags $(TARGET_DIR)/dags
ln -s $(SOURCE_DIR)/logs $(TARGET_DIR)/logs
ln -s $(SOURCE_DIR)/plugins $(TARGET_DIR)/plugins

