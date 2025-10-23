import streamlit as st
import duckdb
import pandas as pd

# Sidinställningar
# Lägga till karta
# Grafer och diagrammer

st.set_page_config(page_title="Jobbstatistik", layout="wide")

st.title("Jobbstatistik från JobTech API")

# Anslut till databasen
con = duckdb.connect("job_ads_pipeline.duckdb")

# Hämta data från tabellen
df = con.execute("""
    SELECT
        occupation AS "Yrkesområde",
        municipality AS "Kommun",
        COUNT(*) AS "Antal annonser"
    FROM job_ads_dataset.job_ads_summary
    GROUP BY occupation, municipality
    ORDER BY "Antal annonser" DESC
""").fetchdf()

# Diagram och tabell
st.subheader("Antal jobbannonser per kommun och yrkesområde")
st.bar_chart(df.set_index("Kommun"))

st.subheader("Detaljerad tabell")
st.dataframe(df)

#streamlit run dashboard.py

