#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example DAG demonstrating the usage of the TaskFlow API to execute Python functions natively and within a
virtual environment.
"""
from __future__ import annotations

import logging
import os
import shutil
import sys
import tempfile
import time
from pprint import pprint

import pendulum

from airflow import DAG
from airflow.decorators import task

log = logging.getLogger(__name__)

PYTHON = sys.executable

BASE_DIR = tempfile.gettempdir()

# This function is run on any failure callback in the other workflows.
def task_failure_alert(context):
    print("Fail works  !  ")
    with open('/Users/kevincheung/DB1.txt', 'w') as file:
        file.write("Rollback")
    with open('/Users/kevincheung/DB2.txt', 'w') as file:
        file.write("Rollback")


with DAG(
    dag_id='basic_workflow_2',
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    on_failure_callback=task_failure_alert,
    tags=['example'],
) as dag:
    # [START howto_operator_python]
    @task(task_id="start")
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs['dag_run'].conf['data'])

        this_stuff=kwargs['dag_run'].conf['data']
        pprint(this_stuff)
        
        print(ds)
        return 'Whatever you return gets printed in the logs'

    run_this = print_context()
    # [END howto_operator_python]

    error = None

    # [START howto_operator_python_kwargs]

    
    # The first task which updates file 1
    @task(task_id=f'update_for_1', on_failure_callback=task_failure_alert)
    def my_updating_function(random_base, **kwargs):

        data_params=kwargs['dag_run'].conf['data']

        pprint(random_base)
        if random_base < 0.1 and data_params == "abc":
            raise Exception("Manual Error")
        
        """This is a function that will run within the DAG execution"""
        time.sleep(random_base)

        with open('/Users/kevincheung/DB1.txt', 'w') as file:
            file.write(str(data_params))

    updating_task = my_updating_function(random_base=0.0)

    run_this >> updating_task

    # The second task which updates file 2. Will throw an error if input for data argument is abc.
    @task(task_id=f'update_for_2', on_failure_callback=task_failure_alert)
    def my_updating_function2(random_base, **kwargs):

        data_params=kwargs['dag_run'].conf['data']

        pprint(random_base)
        if random_base < 0.1 and data_params == "abc":
            raise Exception("Manual Error")
        
        """This is a function that will run within the DAG execution"""
        time.sleep(random_base)

        with open('/Users/kevincheung/DB2.txt', 'w') as file:
            file.write(str(data_params))

    updating_task2 = my_updating_function2(random_base=0.1)

    run_this >> updating_task2

    # [END howto_operator_python_kwargs]
