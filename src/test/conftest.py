"""Conftest file including setting common fixtures.

Common fixtures include a connection to a postgres database, a set of sample model and
 seed files, dbt configuration files, and temporary directories for everything.
"""
import pytest
from airflow import settings
from airflow.models.connection import Connection


@pytest.fixture(scope="session")
def airflow_conns(database):
    """Create Airflow connections for testing.

    We create them by setting AIRFLOW_CONN_{CONN_ID} env variables. Only postgres
    connections are set for now as our testing database is postgres.
    """
    uris = (
        f"postgres://{database.user}:{database.password}@{database.host}:{database.port}/public?dbname={database.dbname}",
        f"postgres://{database.user}:{database.password}@{database.host}:{database.port}/public",
    )
    ids = (
        "dbt_test_postgres_1",
        database.dbname,
    )
    session = settings.Session()

    connections = []
    for conn_id, uri in zip(ids, uris):
        existing = session.query(Connection).filter_by(conn_id=conn_id).first()
        if existing is not None:
            # Connections may exist from previous test run.
            session.delete(existing)
            session.commit()
        connections.append(Connection(conn_id=conn_id, uri=uri))

    session.add_all(connections)

    session.commit()

    yield ids

    session.close()
