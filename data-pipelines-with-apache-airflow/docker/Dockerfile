FROM apache/airflow:2.0.1

USER root
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends vim less && \
    pip install apache-airflow-providers-microsoft-azure==1.2.0rc1
