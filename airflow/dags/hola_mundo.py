from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
import datetime

def Hola_mundo():
    print('Hola mundo :)')

with DAG(
    dag_id='hola_mundo_dag',
    start_date=datetime.datetime(2023, 10, 23),
    tags=['example', 'python'],
) as dag:
    task_1 = PythonOperator(
    task_id='hola_mundo_1',
    python_callable=Hola_mundo
    )

    task_2 = BashOperator(
    task_id='hola_mundo_2',
    bash_command="echo 'Hola mundo, después del primer task!'",
    )

    task_1 >> task_2
