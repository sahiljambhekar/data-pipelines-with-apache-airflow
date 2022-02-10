import airflow.utils.dates
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

dag: DAG = DAG(
    dag_id="01Playground",
    description="Hello World",
    catchup=True,
    schedule_interval="0 16 * * *", # 4 PM EveryDay.
    start_date=datetime(2022, 2, 6, 12) # airflow.utils.dates.days_ago(3),
   # end_date = datetime(2022, 2, 9, 14) #airflow.utils.dates.days_ago(1),
)

bs_op_1 = BashOperator(
    task_id="first_task",
    bash_command='echo "This is the ${order} command for \n${debug_str}\ndates: ${dates_str}" ',
    env={
        "order": "first",
        "debug_str": "run_id={{run_id}} | dag_run={{dag_run}} ",
        "dates_str": "execution_date = {{ds}}  next_execution_date = {{next_ds}}"
    },
    dag=dag
)

bs_op_2 = BashOperator(
    task_id="second_task",
    bash_command='echo "This is the ${order} command for \n${debug_str}\ndates: ${dates_str}" ',
    env={
        "order": "second",
        "debug_str": "run_id={{run_id}} | dag_run={{dag_run}} ",
        "dates_str": "execution_date = {{ds}}  next_execution_date = {{next_ds}}"
    },
    dag=dag
)

where_am_i = BashOperator(
    task_id="where_am_i",
    bash_command='pwd && ls -al',
    dag=dag
)

dummy_join = DummyOperator(task_id="dummy_task", dag=dag)
where_am_i >> [bs_op_1, bs_op_2] >> dummy_join
