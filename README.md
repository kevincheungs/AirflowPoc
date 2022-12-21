# AirflowPoc

## Setting up Airflow
Follow directions to install Airflow server locally

https://airflow.apache.org/docs/apache-airflow/2.1.0/installation.html

Once everything is set up, start Airflow server by running the following

Airflow standalone

## Details about the DAG

1. Place the python file basic_workflow_2.py in the path for where your Airflow server reads the DAGs from. For me it was, 	/opt/homebrew/lib/python3.10/site-packages/airflow/example_dags
2. Login to the Airflow UI (default is http://localhost:8080/) using the username and password given when you started up the Airflow server.
3. Activate the DAG by clicking on the slider next to it.
4. You can click on the item to get more info on it (Grid, Graph, Logs, etc)
![image](https://user-images.githubusercontent.com/84427780/209002819-df26d8f1-80f6-4c0b-93b7-5f5b80dc5d1c.png)

## Running the DAG

In the details section, you can click the play button from the UI to launch the DAG

OR

Through the API

### Postman

Make sure to fill out the Authorization section using the same credentials you logged in with. Otherwise, no special headers needed.
<img width="1006" alt="image" src="https://user-images.githubusercontent.com/84427780/209003653-15256073-def1-4951-820a-5d0c0c37fdd0.png">

URL: POST http://localhost:8080/api/v1/dags/{NAME_OF_DAG}/dagRuns

Example JSON request body

{
    "execution_date": "2022-10-28T09:00:00Z",
    "conf": {
        "data": "dbupdate"
    }
}

As long as execution_date is before the current date time, it should run immediately. If it's in the future, it will be scheduled to run at that time.

The above conf field is accessed in the code by

data_params=kwargs['dag_run'].conf['data']
