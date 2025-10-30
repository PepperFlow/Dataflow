from dagster import job, op
import subprocess
import os


@op(name="extract_and_load_op")
def extract_and_load():
    
    print("--- Startar DLT-pipelinen (load_job_ads_dlt.py) ---")
    
    subprocess.run(["python", "load_job_ads_dlt.py"], check=True)
    
    return True


@op(name="transform_data_op")
def transform_data(start_signal): 
    print("--- Startar dbt-transformation (dbt run) ---")
    
    
    
    subprocess.run(
        ["dbt", "run", "--project-dir", "job_ads_dbt"], 
        check=True
    )
    print("--- dbt-transformation klar ---")


@job(name="job_ads_etl_pipeline")
def job_ads_etl_pipeline():
    
    transform_data(start_signal=extract_and_load())

# OBS: Du behöver också en defs.py som pekar på denna fil om du kör dagster dev
# Om din fil heter 'dagster', kan du behöva döpa om den till 'defs.py'
# eller konfigurera dagster.yaml. Det enklaste är att döpa om den till defs.py.
#inställera # Se till att du har dessa i din requirements.txt och installerade
#pip install dagster dagster-webserver dbt-duckdb
