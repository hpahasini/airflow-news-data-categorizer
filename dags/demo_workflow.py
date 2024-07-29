from __future__ import annotations

import json
import os
from datetime import datetime

from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from news_data_transfomer import transform_news_data, save_to_csv
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.dates import days_ago

dag = DAG(
    "news_data_categorizer",
    default_args={"retries": 1},
    tags=["demo"],
    start_date=datetime(2024, 7, 21),
    schedule_interval='@daily',
    catchup=False,
)

def process_news_data(**kwargs):
    ti = kwargs['ti']
    news_data = ti.xcom_pull(task_ids='get_news_data')
    
    if news_data:
        transformed_data = transform_news_data(news_data)
        file_path = save_to_csv(transformed_data, 'transformed_news')
        ti.xcom_push(key='file_path', value=file_path)
        print(f"CSV file saved at: {file_path}")


def upload_to_s3(**kwargs):
    ti = kwargs['ti']
    file_path = ti.xcom_pull(task_ids='transform_data', key='file_path')
    print(f"File is : {file_path}")
    if file_path:
        s3_hook = S3Hook(aws_conn_id='aws_connection')
        s3_key = f"categorized_news_data/{file_path.split('/')[-1]}"
        bucket_name = 'airflowmlworkflow'
        s3_hook.load_file(filename=file_path, key=s3_key, bucket_name=bucket_name, replace=True)
        print(f"File uploaded to S3 at: s3://{bucket_name}/{s3_key}")


get_news_data = SimpleHttpOperator(
    task_id="get_news_data",
    http_conn_id="http_connection",
    method="GET",
    endpoint="/v2/top-headlines?country=us&apiKey=c6b3fc44ba914a739026696211d59547",
    response_filter = lambda response : json.loads(response.text),
    dag=dag
)

transform_data = PythonOperator(
    task_id = "transform_data",
    python_callable = process_news_data,
    provide_context=True,
    dag=dag
)

upload_to_s3_bucket = PythonOperator(
    task_id="upload_to_s3",
    python_callable=upload_to_s3,
    provide_context=True,
    dag=dag,
)

get_news_data >> transform_data >> upload_to_s3_bucket