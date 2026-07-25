import logging
import duckdb

logger = logging.getLogger(__name__)

def load_raw_observations(warehouse_path: str = 'warehouse.duckdb') -> None:
    """Load all raw JSON files from the data lake into a DuckDB table.

    Uses hive_partitioning so the `date=YYYY-MM-DD` folder structure becomes
    an actual `date` column, rather than being ignored. Full refresh each run
    (CREATE OR REPLACE) — fine at this data volume; a real incremental load
    is a later improvement once Airflow tracks what's already been processed.
    """
    connection = duckdb.connect(warehouse_path)
    connection.sql(
        """
        CREATE OR REPLACE TABLE raw_observations AS
            SELECT *
              FROM read_json_auto(
                'data/raw/observations/*/*.json',
                hive_partitioning = true
              )
        """
    )

    count = connection.sql("SELECT COUNT(*) FROM raw_observations").fetchone()[0]
    logger.info("Loaded %d raw observation rows into DuckDB", count)

    connection.close()
