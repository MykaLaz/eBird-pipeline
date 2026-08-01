from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

PROJECT_DIR = "/Users/marinalazareva/Documents/Data Engineering/eBird-pipeline"
DBT_DIR = f"{PROJECT_DIR}/ebird_analytics"
REGION_CODE = "US-NY"

with DAG(
    dag_id="ebird_daily_pipeline",
    description="Daily eBird ingestion, warehouse load, and dbt transform",
    schedule="@daily",
    start_date=datetime(2026, 7, 1),
    catchup=False,
    tags=["ebird"],
) as dag:

    fetch_yesterday = BashOperator(
        task_id="fetch_yesterday",
        bash_command=f'cd "{PROJECT_DIR}" && uv run python main.py backfill {REGION_CODE} --days 1',
    )

    load_warehouse = BashOperator(
        task_id="load_warehouse",
        bash_command=f'cd "{PROJECT_DIR}" && uv run python main.py load',
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f'cd "{DBT_DIR}" && uv run dbt run',
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f'cd "{DBT_DIR}" && uv run dbt test',
    )

    fetch_yesterday >> load_warehouse >> dbt_run >> dbt_test
