from dagster import job, op, Definitions
import subprocess

@op(name="extract_and_load_op")
def extract_and_load():
    print("--- Startar DLT-pipelinen ---")
    subprocess.run(["python", "load_job_ads_dlt.py"], check=True)
    return True

@op(name="transform_data_op")
def transform_data(start_signal): 
    print("--- Startar dbt-transformation ---")
    subprocess.run(
        ["dbt", "run", "--project-dir", "job_ads_dbt"], 
        check=True
    )
    print("--- dbt-transformation klar ---")

@job(name="job_ads_etl_pipeline")
def job_ads_etl_pipeline():
    transform_data(start_signal=extract_and_load())

# VIKTIGT: Detta är vad Dagster letar efter!
defs = Definitions(
    jobs=[job_ads_etl_pipeline]
)
