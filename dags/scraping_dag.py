from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.scraping.id_scraper import id_scraper
from src.scraping.property_scraper import property_scraper
from src.scraping.json_to_csv import json_to_csv

default_args = {
    'owner': 'admin',
    'retry': 5,
    'retry_delay': timedelta(minutes=1)
}

with DAG(

    default_args=default_args,
    dag_id='scraping_dag_v2',
    start_date=datetime(2023, 9, 18),
    schedule_interval='@once',
    catchup=False,




) as dag:

    get_ids = PythonOperator(
        task_id='get_ids',
        python_callable=id_scraper,
        op_kwargs={"pages": 1},
    )

    get_properties = PythonOperator(
        task_id='get_properties',
        python_callable=property_scraper,
    )

    to_csv = PythonOperator(
        task_id='to_csv',
        python_callable=json_to_csv,
    )

    get_ids >> get_properties >> to_csv
