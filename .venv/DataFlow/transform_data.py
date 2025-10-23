import duckdb

# Anslut till databasen
con = duckdb.connect("job_ads_pipeline.duckdb")

# Kör SQL-filen
with open("transform_data.sql", "r") as f:
    sql_script = f.read()
    con.execute(sql_script)

print(" Transformation klar  tabellen job_ads_summary skapad")

print(con.execute("SELECT * FROM job_ads_dataset.job_ads_summary LIMIT 5").fetchdf())
