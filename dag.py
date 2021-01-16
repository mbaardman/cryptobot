"""
Author: Marc Baardman
"""
# Import airflow packages
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

# import non-airflow packages
import config
from datetime import timedelta, datetime

if config.prod_flow:
    dag_name = 'Production'
else:
    dag_name = 'Testing'

markets = DAG(
    dag_name,
    default_args=config.airflow_default_args,
    description='Run all processes.',
    schedule_interval=config.airflow_schedule_interval
)

for market in config.list_markets:
    command = 'python {0} {1}'.format(config.run_scripts_path, market)
    operation = BashOperator(
        task_id = market,
        bash_command=command,
        dag=markets,
    )
