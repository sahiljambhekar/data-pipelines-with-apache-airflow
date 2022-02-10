#!/bin/sh
source ../venv/bin/activate
alias python3=$(which python3)

AIRFLOW_VERSION=2.2.3

export AIRFLOW_HOME=~/airflows/2.2
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.8
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
NUMPY_VERSION=$(curl -sL -XGET $CONSTRAINT_URL | grep numpy)
echo "${CONSTRAINT_URL} ${NUMPY_VERSION}"
# https://tilcode.blog/2021/06/14/how-to-install-numpy-and-pandas-for-data-science-in-a-m1-macbook/
pip3 install Cython
pip3 install --no-binary :all: --no-use-pep517 ${NUMPY_VERSION}
pip3 install -r ../requirements.txt --constraint "${CONSTRAINT_URL}"
# https://airflow.apache.org/docs/apache-airflow/1.10.3/installation.html

airflow standalone