import dlt
import requests

# Källa 
@dlt.source
def jobtech_source(occupation: str):
    @dlt.resource(name=f"job_ads_{occupation}", write_disposition="replace")
    def job_ads():
        url = "https://jobsearch.api.jobtechdev.se/search"
        params = {"q": occupation, "limit": 50}
        data = requests.get(url, params=params).json()

        for ad in data.get("hits", []):
            yield {
                "title": ad.get("headline"),
                "employer": ad.get("employer", {}).get("name"),
                "municipality": ad.get("workplace_address", {}).get("municipality"),
                "occupation": occupation
            }

    return job_ads

# Kör pipelinen 
if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="job_ads_pipeline",
        destination="duckdb",
        dataset_name="job_ads_dataset"
    )

    occupations = ["data", "hr", "ekonomi"]
    for occ in occupations:
        data = jobtech_source(occ)
        pipeline.run(data)
        print("Data laddad till DuckDB: job_ads_pipeline.duckdb")
