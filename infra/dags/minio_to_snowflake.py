import os
import boto3
import snowflake.connector
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# -----------------------
# MinIO Settings
# -----------------------
MINIO_ENDPOINT = "http://minio:9000"
MINIO_ACCESS_KEY = "Sirisha"
MINIO_SECRET_KEY = "Sirisha123"
BUCKET = "bronze-transactions"
LOCAL_DIR = "/tmp/minio_downloads"

# -----------------------
# Snowflake Settings
# -----------------------
SNOWFLAKE_USER = "Sirisha"
SNOWFLAKE_PASSWORD = "Gajulasirisha@1617"
SNOWFLAKE_ACCOUNT = "vu87888.ca-central-1.aws"

SNOWFLAKE_ROLE = "ACCOUNTADMIN"
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
SNOWFLAKE_DB = "STOCKS_MDS"
SNOWFLAKE_SCHEMA = "STOCKS_MDS_COMMON"

# IMPORTANT: set to your real table name (exactly as created)
TARGET_TABLE = "BRONZE_STOCK_QUOTES_RAW"


def download_from_minio():
    os.makedirs(LOCAL_DIR, exist_ok=True)

    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )

    objects = s3.list_objects_v2(Bucket=BUCKET).get("Contents", [])
    local_files = []

    for obj in objects:
        key = obj["Key"]
        local_file = os.path.join(LOCAL_DIR, os.path.basename(key))
        s3.download_file(BUCKET, key, local_file)
        print(f"Downloaded {key} -> {local_file}")
        local_files.append(local_file)

    return local_files


def load_to_snowflake(**kwargs):
    ti = kwargs["ti"]
    local_files = ti.xcom_pull(task_ids="download_minio") or []

    if not local_files:
        print("No files to load.")
        return

    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
    )

    cur = conn.cursor()
    try:
        cur.execute(f'USE ROLE "{SNOWFLAKE_ROLE}"')
        cur.execute(f'USE WAREHOUSE "{SNOWFLAKE_WAREHOUSE}"')
        cur.execute(f'USE DATABASE "{SNOWFLAKE_DB}"')
        cur.execute(f'USE SCHEMA "{SNOWFLAKE_DB}"."{SNOWFLAKE_SCHEMA}"')

        # Named stage + table (fully qualified)
        stage_name = f'"{SNOWFLAKE_DB}"."{SNOWFLAKE_SCHEMA}"."BRONZE_STAGE"'
        target_table = f'"{SNOWFLAKE_DB}"."{SNOWFLAKE_SCHEMA}"."{TARGET_TABLE}"'

        # Ensure stage exists (safe)
        cur.execute(f"CREATE STAGE IF NOT EXISTS {stage_name}")

        # Upload files
        for f in local_files:
            cur.execute(f'PUT file://{f} @{stage_name} AUTO_COMPRESS=FALSE OVERWRITE=TRUE')
            print(f"Uploaded {f} -> @{stage_name}")

        # Copy into table (raw JSON -> VARIANT)
        cur.execute(f"""
            COPY INTO {target_table}
            FROM (SELECT $1, CURRENT_TIMESTAMP() FROM @{stage_name})
            FILE_FORMAT = (TYPE = JSON)
            ON_ERROR = 'CONTINUE'
        """)
        print("COPY INTO executed successfully.")

    finally:
        cur.close()
        conn.close()


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 2, 19),
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    "minio_to_snowflake",
    default_args=default_args,
    schedule_interval="*/1 * * * *",
    catchup=False,
) as dag:

    task1 = PythonOperator(
        task_id="download_minio",
        python_callable=download_from_minio,
    )

    task2 = PythonOperator(
        task_id="load_snowflake",
        python_callable=load_to_snowflake,
        provide_context=True,
    )

    task1 >> task2