"""Test dbt operators with multiple testing DAGs."""
from __future__ import annotations

import datetime as dt

import pendulum
import pytest

from airflow import settings
from airflow.models import DagBag, DagRun
from airflow.models.serialized_dag import SerializedDagModel

DATA_INTERVAL_START = pendulum.datetime(2022, 1, 1, tz="UTC")
DATA_INTERVAL_END = DATA_INTERVAL_START + dt.timedelta(hours=1)



airflow = pytest.importorskip("airflow", minversion="2.2")


@pytest.fixture(scope="session")
def dagbag():
    """An Airflow DagBag."""
    dagbag = DagBag(dag_folder="examples/", include_examples=False)

    return dagbag


def test_dags_loaded(dagbag):
    """Assert DAGs have been properly loaded."""
    assert dagbag.import_errors == {}

    for dag_id in dagbag.dag_ids:
        dag = dagbag.get_dag(dag_id=dag_id)

        assert dag is not None


@pytest.fixture(scope="function")
def clear_dagruns():
    """Ensure we are starting from a clean DagRun table."""
    session = settings.Session()
    session.query(DagRun).delete()
    session.commit()

    yield

    session.query(DagRun).delete()
    session.commit()
    # We delete any serialized DAGs too for reproducible test runs.
    session.query(SerializedDagModel)
    session.commit()
