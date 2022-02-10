from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator


dag = DAG(
    dag_id="01_unscheduled", start_date=datetime(2019, 1, 1), schedule_interval=None
)

output_dir = "/tmp/airflow/data/events"

where_am_i = BashOperator(
    task_id="where_am_i",
    bash_command=(
        f"pwd && "
        f"ls -alr"
    ),
    dag=dag,
)

error_out = BashOperator(
    task_id="error_out",
    bash_command="ls-alr",
    dag=dag,
)


fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        f"mkdir -p {output_dir} && "
        f"curl -o {output_dir}/events.json http://events_api:5000/events"
    ),
    dag=dag,
)


def _calculate_stats(input_path, output_path):
    """Calculates event statistics."""

    Path(output_path).parent.mkdir(exist_ok=True)

    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()

    stats.to_csv(output_path, index=False)


calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    op_kwargs={"input_path": f"{output_dir}/events.json", "output_path": f"{output_dir}/stats.csv"},
    dag=dag,
)

dummy = DummyOperator(dag=dag,task_id="dummy")

fetch_events >> calculate_stats
where_am_i >> error_out
#[calculate_stats,error_out] >> dummy
