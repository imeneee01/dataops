from __future__ import annotations

import os
from datetime import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

RAW_DIR = os.environ.get("RAW_DIR", "/opt/airflow/data/raw")
PROCESSED_DIR = os.environ.get("PROCESSED_DIR", "/opt/airflow/data/processed")
PIPELINE_IMAGE = os.environ.get("PIPELINE_IMAGE", "customers-pipeline:latest")

with DAG(
    dag_id="dataops_customers_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dataops", "docker"],
) as dag:

    run_pipeline = DockerOperator(
        task_id="run_pipeline_container",
        image=PIPELINE_IMAGE,
        api_version="auto",
        auto_remove="never",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mount_tmp_dir=False,
        mounts=[
            Mount(source="data-raw", target="/app/data/raw", type="volume"),
            Mount(source="data-processed", target="/app/data/processed", type="volume"),
        ],
    )