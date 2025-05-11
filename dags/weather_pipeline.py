import sys
import os
sys.path.insert(0, '/opt/airflow')

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.data.gather_data import collect_weather_data
from src.preprocessing.preprocess_data import preprocess_data

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 5, 3),
    "retries": 1,
}

dag = DAG(
    "weather_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
)

collect_task = PythonOperator(
    task_id="collect_data",
    python_callable=collect_weather_data,
    dag=dag,
)

preprocess_task = PythonOperator(
    task_id="preprocess_data",
    python_callable=preprocess_data,
    dag=dag,
)

collect_task >> preprocess_task
