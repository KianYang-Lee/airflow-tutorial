"""
An example demonstrating how to get some data from a file which is hosted online 
and insert into local DB (postgres), at the same time
removing duplicate rows while populating the table.
"""

from airflow.decorators import dag, task
from datetime import datetime, timedelta
import requests

@dag(
    dag_id="my_postgres_dag",
    schedule_interval="0 0 * * *",
    start_date=datetime.today() - timedelta(days=2),
    dagrun_timeout=timedelta(minutes=60),
)
def Etl():
    @task
    def get_data():
        url = "https://raw.githubusercontent.com/apache/airflow/main/docs/apache-airflow/pipeline_example.csv"

        response = requests.request("GET", url)

        with open("/usr/local/airflow/dags/files/employees.csv", "w") as file:
            for row in response.text.split("\n"):
                file.write(row)

        postgres_hook = PostgresHook(postgres_conn_id="LOCAL")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
        with open("/usr/local/airflow/dags/files/employees.csv", "r") as file:
            cur.copy_from(
                f,
                "Employees_temp",
                columns=[
                    "Serial Number",
                    "Company Name",
                    "Employee Markme",
                    "Description",
                    "Leave",
                ],
                sep=",",
            )
        conn.commit()

    @task
    def merge_data():
        query = """
                delete
                from "Employees" e using "Employees_temp" et
                where e."Serial Number" = et."Serial Number";

                insert into "Employees"
                select *
                from "Employees_temp";
                """
        try:
            postgres_hook = PostgresHook(postgres_conn_id="LOCAL")
            conn = postgres_hook.get_conn()
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            return 0
        except Exception as e:
            return 1

    get_data() >> merge_data()


dag = Etl()