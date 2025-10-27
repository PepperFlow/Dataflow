import duckdb
import os

db_path = "job_ads_pipeline.duckdb"
if not os.path.exists(db_path):
    print("DuckDB-filen hittades inte:", db_path)
    raise SystemExit(1)

con = duckdb.connect(db_path)

print("\n📂 Scheman i databasen:")
schemas = con.execute("SELECT schema_name FROM information_schema.schemata").fetchall()
for s in schemas:
    print(" -", s[0])

print("\n📊 Tabeller i job_ads_dataset:")
tables = con.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'job_ads_dataset'
""").fetchall()

if not tables:
    print("⚠️ Ingen tabell hittades i schemat job_ads_dataset.")
else:
    print("Tabeller:", tables)
    for t in tables:
        name = t[0]
        print(f"\n🔹 Förhandsgranskning av {name}:")
        df = con.execute(f"SELECT * FROM job_ads_dataset.{name} LIMIT 5").fetchdf()
        print(df)
