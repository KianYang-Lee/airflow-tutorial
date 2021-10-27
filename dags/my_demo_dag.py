from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from data_scrapper import scrap_joke
from model_trainer import inference, generate_model

args = {"owner": "Kian Yang Lee", "start_date": days_ago(1)}

dag = DAG(dag_id="my_demo_dag", default_args=args, schedule_interval="0 * * * *")

with dag:
    scrap_joke_task = PythonOperator(
        task_id="scrap_joke",
        python_callable=scrap_joke,
    )

    train_model_task = PythonOperator(
        task_id="train_model",
        python_callable=generate_model,
    )

    inference_task = PythonOperator(
        task_id="inference",
        python_callable=inference,
    )

    scrap_joke_task >> train_model_task >> inference_task
    # Even if you do not set up the dependencies, each individual task will still run
    # scrap_joke_task >> train_model_task
