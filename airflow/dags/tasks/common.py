from airflow.decorators import task

from utils.schemas import DagMetaData


@task()
def notify_owner(dag_params: DagMetaData):
    from airflow.utils.email import send_email
    send_email(to=dag_params.notify,
               subject=f"Dag for {dag_params.project} completed",
               html_content=f"Dag finished successfully!")
