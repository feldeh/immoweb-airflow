from airflow.models import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta
from airflow.sensors.time_delta import TimeDeltaSensor


default_args = {
    'owner': 'admin',
    'retry': 5,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='master_dag',
    start_date=datetime(2023, 9, 21),
    schedule_interval='@once',
    catchup=False,

) as dag:

    trigger_scraping = TriggerDagRunOperator(
        task_id='trigger_scraping',
        trigger_dag_id='scraping_dag_v2',
    )

    # delay_cleaning = TimeDeltaSensor(
    #     task_id='delay_cleaning',
    #     delta=timedelta(seconds=20)
    # )

    trigger_cleaning = TriggerDagRunOperator(
        task_id='trigger_cleaning',
        trigger_dag_id='cleaning_dag',
    )


trigger_scraping >> trigger_cleaning
# trigger_scraping >> delay_cleaning >> trigger_cleaning
