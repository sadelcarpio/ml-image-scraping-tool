from airflow.decorators import task
from airflow.utils.trigger_rule import TriggerRule

from utils.schemas import DagMetaData


@task(task_id="notify_owner", trigger_rule=TriggerRule.ALWAYS)
def notify_owner(dag_params: DagMetaData):
    from airflow.utils.email import send_email
    send_email(to=dag_params.notify,
               subject=f"Dag for {dag_params.project} completed",
               html_content=f"Dag finished successfully!")
