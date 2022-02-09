#!/bin/zsh
cd ..
source ../venv/bin/activate
AIRFLOW_VERSION=2.2.3

export AIRFLOW_HOME=~/airflows/2.2
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.8
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install -r requirements.txs --constraint "${CONSTRAINT_URL}"
# https://airflow.apache.org/docs/apache-airflow/1.10.3/installation.html

airflow standalone