import duckdb
import os

# Ange sökvägen till din DuckDB-fil
db_path = "job_ads_pipeline.duckdb"

# Kontrollera att filen finns
if not os.path.exists(db_path):
    print(f"Hittar inte databasen: {db_path}")
    print("Kör först test_jobtech_api.py för att skapa filen.")
    exit()

# Anslut till databasen
con = duckdb.connect(db_path)

print(f" Ansluten till databasen: {db_path}\n")

# Visa alla tabeller
tables = con.execute("SHOW TABLES").fetchall()
if not tables:
    print("⚠️  Inga tabeller hittades i databasen.")
    print("Kör om din pipeline (test_jobtech_api.py) och försök igen.")
else:
    print("📊 Tabeller i databasen:")
    for t in tables:
        print("  -", t[0])

    # Visa några rader ur varje tabell
    for t in tables:
        name = t[0]
        print(f"\n Förhandsgranskning av tabell: {name}")
        try:
            df = con.execute(f"SELECT * FROM {name} LIMIT 5").fetchdf()
            print(df)
        except Exception as e:
            print(f"Fel vid läsning av tabell {name}: {e}")

print("\n Klart! Du kan nu se vilka tabeller och data DLT har skapat i DuckDB.")
