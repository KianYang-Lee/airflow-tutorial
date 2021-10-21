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
  4. [Configure tasks for individual DAG object](#step-4-configure-tasks-for-individual-dag-object)
  5. [Configure tasks dependencies](#step-5-configure-tasks-dependencies)
- [Execute DAGs](#execute-dags)
- [Monitor Workflow Using Airflow UI](#monitor-workflow-using-airflow-ui)
- [References](#references)

## Introduction to Apache Airflow
A slide deck which provides brief introduction on what is Apache Airflow, why use Airflow, where is it suitable to use Airflow, and when to use Airflow can be found [here](#).

## Getting Started
We are going to use Docker containers to spin up Airflow container as we also need to spin up container for other services. Follow the steps below to get Apache Airflow up and running using Docker container:

1. Clone this repo
2. Configure host user id
```echo -e "AIRFLOW_UID=$(id -u)" > .env```

3. Initialize the database and create first user account
```docker-compose up airflow-init```

You should see similar message as below that indicates success execution:
```
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

### Step 1: Import Libraries
### Step 2: Configure default arguments
### Step 3: Instantiate DAG object
### Step 4: Configure tasks for individual DAG object
### Step 5: Configure tasks dependencies

## Execute DAGs

To execute or trigger a DAG manually, first unpause a DAG.

Next, click on the DAG and the "play" button on top right.

The UI will display the execution status after that.

## Monitor Workflow Using Airflow UI

To check out on the details of tasks, click on the task shape in the UI.

Then, select the details which you would like to check out. Log and graph are among useful details which you should check out.

## References
- [Airflow tutorial 4: Writing your first pipeline](https://www.youtube.com/watch?v=43wHwwZhJMo)
- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
- [How to Run Your First Airflow DAG in Docker](https://predictivehacks.com/how-to-run-your-first-airflow-dag-in-docker/)
- [Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)