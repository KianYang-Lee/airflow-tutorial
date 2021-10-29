# Airflow-Tutorial
Contains tutorial on getting started in using Apache Airflow to automate pipelines.

## Contents
- [Introduction to Apache Airflow](#introduction-to-apache-airflow)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Write an Airflow DAG](#write-an-airflow-dag)

  1. [Import libraries](#step-1-import-libraries)
  2. [Configure default arguments](#step-2-configure-default-arguments)
  3. [Instantiate DAG object](#step-3-instantiate-dag-object)
  4. [Configure tasks by instantiating operators](#step-4-configure-tasks-by-instantiating-operators)
  5. [Configure tasks dependencies](#step-5-configure-tasks-dependencies)
- [Execute DAGs](#execute-dags)
- [Monitor Workflow Using Airflow UI](#monitor-workflow-using-airflow-ui)
- [Interact with Docker Container](#interact-with-docker-container)
- [References](#references)

## Introduction to Apache Airflow
A slide deck which provides brief introduction on what is Apache Airflow, why use Airflow, where is it suitable to use Airflow, and when to use Airflow can be found [here](#).

## Getting Started
We are going to use Docker containers to spin up Airflow container as we also need to spin up container for other services. Follow the steps below to get Apache Airflow up and running using Docker container:

1. Clone this repo.
2. Configure host user id, additional Python packages and directories:

```sh
echo -e "AIRFLOW_UID=$(id -u)\n_PIP_ADDITIONAL_REQUIREMENTS=pymongo pandas scikit-learn apache-airflow-providers-mongo" > .env && mkdir -p dags logs plugins
```

3. Initialize the database and create first user account:
```sh
docker-compose up airflow-init
```

You should see similar message as below that indicates success execution:
```sh
airflow-init_1       | User "airflow" created with role "Admin"
airflow-init_1       | 2.2.0
airflow-tutorial_airflow-init_1 exited with code 0
```

4. Start all services:
```docker-compose up```

5. Visit [localhost:8080](http://localhost:8080). The default username and password are both `airflow`.

6. Spin down the containers by:
```docker-compose down```

To completely remove the containers, volumes with DB data and downloaded images, run:
```docker-compose down --volumes --rmi all```

Alternatively, you can install it via PyPi by following the instructions [here](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html#using-pypi).

## Prerequisites
- Installed Docker [[manual]](https://docs.docker.com/get-docker/)
- Installed Docker-compose [[manual]](https://docs.docker.com/compose/install/)
- At least 4GB memory for Docker Engine 

## Write an Airflow DAG
DAG stands for directed acyclic graph, which is a collection of tasks which constitute a pipeline/workflow. The steps below are required to construct a DAG.

- Step 1: Import Libraries
- Step 2: Configure default arguments
- Step 3: Instantiate DAG object
- Step 4: Configure tasks by instantiating operators
- Step 5: Configure tasks dependencies

## Execute DAGs

To execute or trigger a DAG manually, first unpause a DAG.

Next, click on the DAG and the "play" button on top right.

The UI will display the execution status after that.

## Monitor Workflow Using Airflow UI

To check out on the details of tasks, click on the task shape in the UI.

Then, select the details which you would like to check out. Log and graph are among useful details which you should check out.

## Interact with Docker Container

You might want to interact with the Airflow environment. To do so, execute the following and copy the container ID for airflow-worker service:

```docker ps```

Then run the following to get a bash terminal (remember to replace the right container ID):

```docker exec -it <CONTAINER_ID> bash```

You can then inspect the environment, for example we check all the DAGs available by:

```sh
ls -ltr dags/
```

## References
- [Airflow tutorial 4: Writing your first pipeline](https://www.youtube.com/watch?v=43wHwwZhJMo)
- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
- [How to Run Your First Airflow DAG in Docker](https://predictivehacks.com/how-to-run-your-first-airflow-dag-in-docker/)
- [Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)
- [PostgreSQL Connection](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/connections/postgres.html#howto-connection-postgres)
- [Psycopg2: PostgreSQL & Python the Old Fashioned Way](https://hackersandslackers.com/psycopg2-postgres-python/)
- [Managing Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html)
- [Keep TFIDF result for predicting new content using Scikit for Python](https://stackoverflow.com/questions/29788047/keep-tfidf-result-for-predicting-new-content-using-scikit-for-python)
- [Multi-Class Text Classification with Scikit-Learn](https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f)
- [MongoDB 3.2 authentication failed](https://stackoverflow.com/questions/42912755/how-to-create-a-db-for-mongodb-container-on-start-up)
- [Airflow Schedule Interval 101](https://towardsdatascience.com/airflow-schedule-interval-101-bbdda31cc463)