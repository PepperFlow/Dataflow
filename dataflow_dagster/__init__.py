from dagster import Definitions
from .etl_job import etl_job  

defs = Definitions(jobs=[etl_job])