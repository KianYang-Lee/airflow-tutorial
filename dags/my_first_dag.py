from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
args = {

    'owner': 'Kian Yang Lee',
    'start_date': days_ago(1)
}

dag = DAG(dag_id = 'my_first_dag', default_args=args, schedule_interval=None)


def my_first_print():
    print('This is the first print statement in my first dag.')

def my_second_print():
    print('Which makes this my second print statement.')


with dag:
    run_this_task_first = PythonOperator(
        task_id='1st_print',
        python_callable = my_first_print
    )

    run_this_task_second = PythonOperator(
        task_id='2nd_print',
        python_callable = my_second_print
    )

    run_this_task_first >> run_this_task_second