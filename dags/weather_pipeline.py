import sys
import os
sys.path.insert(0, '/opt/airflow')

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.data.gather_data import collect_weather_data
from src.preprocessing.preprocess_data import preprocess_data
from src.models.train_model import train_model

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

train_task = PythonOperator(
    task_id="train_model",
    python_callable=train_model,
    dag=dag,
)

collect_task >> preprocess_task >> train_task
