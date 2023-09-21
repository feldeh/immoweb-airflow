from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from airflow.sensors.python import PythonSensor
from airflow.sensors.time_delta import TimeDeltaSensor
from src.training.training import train_eval_save_model
from pathlib import Path


def check_csv_exists():
    read_path = Path.cwd() / 'data' / 'cleaned_data.csv'
    if read_path.is_file():
        return True
    return False


default_args = {
    'owner': 'admin',
    'retry': 5,
    'retry_delay': timedelta(seconds=3)
}

with DAG(

    default_args=default_args,
    dag_id='training_dag',
    start_date=datetime(2023, 9, 18),
    schedule_interval='@once',
    catchup=False,




) as dag:

    delay_training = TimeDeltaSensor(
        task_id='delay_training',
        delta=timedelta(seconds=8)
    )

    wait_for_csv = PythonSensor(
        task_id='wait_for_csv',
        python_callable=check_csv_exists,
    )

    training = PythonOperator(
        task_id='training',
        python_callable=train_eval_save_model,
    )

delay_training >> wait_for_csv >> training
