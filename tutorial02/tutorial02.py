import json
import pendulum
from datetime import timedelta
from airflow.decorators import dag, task


@dag(
    schedule=timedelta(days=1),
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def tutorial02():
    """
    ### TaskFlow API Example
    This is an example dag which uses the TaskFlow API, Tutorial02
    """

    @task()
    def extract():
        """
        #### Extract task
        Simple json extraction task
        """
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        order_data_dict = json.loads(data_string)
        return order_data_dict

    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        """
        ### Transform task
        Returns total order value
        """
        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value
        return {"total_order_value": total_order_value}

    @task()
    def load(total_order_value: float):
        """
        ### Load task
        Prints out total order value
        """
        print(f"Total order value is: {total_order_value:.2f}")

    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])


tutorial02()
