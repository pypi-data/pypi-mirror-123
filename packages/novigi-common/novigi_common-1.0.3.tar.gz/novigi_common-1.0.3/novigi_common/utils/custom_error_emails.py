import airflow
from airflow import DAG
import traceback
from airflow.exceptions import (
    AirflowException,
    AirflowFailException,
    AirflowRescheduleException,
    AirflowSkipException,
    AirflowTaskTimeout,
)
from airflow.operators.email_operator import EmailOperator
from airflow.operators import BashOperator, PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.models import Variable
from datetime import datetime, timedelta


def error_email_sender_file_process_failure(context, source_file):
    data_file_name = source_file
    exception = context.get("exception")
    date_and_time = datetime.today()
    etl_job_name = context["task_instance"].dag_id
    params = {
        "etl_job_name": etl_job_name,
        "data_file_name": data_file_name,
        "exception": str(exception),
        "date_and_time": str(date_and_time),
    }
    html_content = Variable.get("email_templates_file_process_failure").format(**params)
    send_email = EmailOperator(
        trigger_rule=TriggerRule.ONE_FAILED,
        mime_charset="utf-8",
        task_id="t1Failed",
        to=[Variable.get("notification_email")],
        subject="IFS " + etl_job_name + " data pipeline failed - " + str(date_and_time),
        html_content=html_content,
    )

    send_email.execute(context=context)


def error_email_sender_sharepoint_api_failure(context):
    # if context["task_instance"].task_id == "get_access_token":
    #     exception = "Error occurred when retrieving auth token"
    # else:
    #     exception = context.get("exception")
    exception = "Error occurred when retrieving auth token"
    date_and_time = datetime.today()
    etl_job_name = context["task_instance"].dag_id
    params = {
        "etl_job_name": etl_job_name,
        "exception": str(exception),
        "date_and_time": str(date_and_time),
    }
    html_content = Variable.get("email_templates_sharepoint_api_failure").format(**params)
    send_email = EmailOperator(
        trigger_rule=TriggerRule.ONE_FAILED,
        mime_charset="utf-8",
        task_id="t1Failed",
        to=[Variable.get("notification_email")],
        subject="IFS " + etl_job_name + " data pipeline failed - " + str(date_and_time),
        html_content=html_content,
    )

    send_email.execute(context=context)


def error_email_sender_db_connection_failure(context, db_name):
    exception = context.get("exception")
    date_and_time = datetime.today()
    etl_job_name = context["task_instance"].dag_id
    params = {
        "etl_job_name": etl_job_name,
        "data_base_name": db_name,
        "exception": str(exception),
        "date_and_time": str(date_and_time),
    }
    html_content = Variable.get("email_templates_db_connection_failure").format(**params)
    send_email = EmailOperator(
        trigger_rule=TriggerRule.ONE_FAILED,
        mime_charset="utf-8",
        task_id="t1Failed",
        to=[Variable.get("notification_email")],
        subject="IFS " + etl_job_name + " data pipeline failed - " + str(date_and_time),
        html_content=html_content,
    )

    send_email.execute(context=context)
