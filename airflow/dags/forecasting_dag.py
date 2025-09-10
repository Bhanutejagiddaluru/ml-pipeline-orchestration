from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.ingest import ingest
from src.featurize import featurize
from src.train import train as train_model
from src.evaluate import evaluate
from src.register import register

with DAG('forecasting_dag', start_date=datetime(2024,1,1), schedule_interval=None, catchup=False) as dag:
    t1=PythonOperator(task_id='ingest', python_callable=lambda: ingest('data/retail_sales_small.csv'))
    t2=PythonOperator(task_id='featurize', python_callable=lambda ti: featurize(ti.xcom_pull(task_ids='ingest')))
    t3=PythonOperator(task_id='train', python_callable=lambda ti: train_model(ti.xcom_pull(task_ids='featurize')))
    t4=PythonOperator(task_id='evaluate', python_callable=lambda ti: evaluate(ti.xcom_pull(task_ids='featurize'), ti.xcom_pull(task_ids='train')))
    t5=PythonOperator(task_id='register', python_callable=lambda ti: register(ti.xcom_pull(task_ids='train')))
    t1>>t2>>t3>>[t4,t5]
