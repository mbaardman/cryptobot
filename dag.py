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
import os
from cryptobot import alerts


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

files = os.listdir(config.scripts_folder)

for file in files:
    try:
        command = 'python {0}/{1}'.format(config.scripts_folder, file)
        operation = BashOperator(
            task_id = file.split('.')[0],
            bash_command=command,
            dag=markets,
        )
    except:
        alert = alerts.SMSAlerts(config.twilio_account, config.twilio_token, config.twilio_from_phone, config.twilio_to_phone)
        alert.alert('Script {} can not be executed.'.format(file))