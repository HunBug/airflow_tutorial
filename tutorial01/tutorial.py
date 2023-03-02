"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.apache.org/tutorial.html)
"""

from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    "Tutorial01",
    default_args={
        "depends_on_past": False,
        "email": ["some@address.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="First tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
    dag.doc_md = __doc__

    task1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    task1.doc_md = dedent(
        """\
        ### Task1 Documentation
        Here comes the documentation for the task1
        """
    )

    task2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3,
    )

    task2.doc_md = dedent(
        """\
        ### Task2 Documentation
        This is the documentation for the task2
        """
    )

    task3_template_command = dedent(
        """\
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7) }}"
        {% endfor %}
        """
    )

    task3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=task3_template_command,
    )

    task1 >> [task2, task3]
