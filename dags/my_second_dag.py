"""
My second dag.
"""

# Step 1: Import libraries
from datetime import datetime, timedelta
from textwrap import dedent
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator

# Step 2: Configure default arguments
#   These args will get passed on to each operator and can be overrided
default_args = {
    "owner": "Kian Yang Lee",
    "depends_on_past": False,
    "email": ["kianyang.lee@certifai.ai"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

# Step 3: Instantiate DAG object
with DAG(
    "my_second_dag",
    default_args=default_args,
    description="A simple tutorial DAG",
    schedule_interval="@daily",  # Either datetime, cron or cron presets
    start_date=datetime(2021, 1, 1),
    catchup=False,  # This disables past tasks from being executed
    tags=["my_second_dag"],
) as dag:

    # Step 4: Configure tasks by instantiating operators
    #   An object instantiated from operators is called a task
    task_1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    task_2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3,
    )
    task_1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)

    """
    )

    dag.doc_md = __doc__  # Display docstring at the beginning of module
    dag.doc_md = """
    This is a documentation placed at the middle of module.
    """  # otherwise, specify it this way

    # Jinja templating
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
    """
    )

    task_3 = BashOperator(
        task_id="Jinja_template",
        depends_on_past=False,
        bash_command=templated_command,
        params={"my_param": "My params are awesome"},
    )

    # Step 5: Configure tasks dependencies
    # This is also equivalent to:
    # task_1 >> [task_2, task_3]
    task_1.set_downstream([task_2, task_3])
