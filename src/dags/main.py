from __future__ import annotations

import pendulum
import pytz
from datetime import datetime, time
from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.utils.trigger_rule import TriggerRule

with DAG(
    dag_id="example_short_circuit_operator",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:

    def check_if_day():
        tz = pytz.timezone("Europe/Berlin")
        now = datetime.now(tz)
        print(now)
        if time(7) < now.time() <= time(19):
            return True
        else:
            return False

    def check_if_nght():
        tz = pytz.timezone("Europe/Berlin")
        now = datetime.now(tz)
        print(now)
        if time(19) < now.time() <= time(24) or time(0) <= now.time() <= time(7):
            return True
        else:
            return False

    cond_true_day = ShortCircuitOperator(
        task_id="cond_true_day",
        ignore_downstream_trigger_rules=False,
        python_callable=check_if_day,
    )

    cond_true_night = ShortCircuitOperator(
        task_id="cond_true_night",
        ignore_downstream_trigger_rules=False,
        python_callable=check_if_nght,
    )

    [task_1, task_2, task_3, task_4, task_5] = [
        EmptyOperator(task_id=f"task_{i}") for i in range(1, 6)
    ]

    task_6 = EmptyOperator(task_id="task_6", trigger_rule=TriggerRule.ALL_DONE)

    chain(
        task_1,
        [cond_true_day, cond_true_night],
        [task_2, task_3],
        [task_4, task_5],
        task_6,
    )
