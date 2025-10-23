import streamlit as st
import duckdb
import pandas as pd

# Sidinställningar
st.set_page_config(page_title="Jobbstatistik", layout="wide")

# Titel
st.title("Jobbstatistik från JobTech API")

# Anslut till databasen
con = duckdb.connect("job_ads_pipeline.duckdb")

# Kolla vilka tabeller som finns
tables = con.execute("SHOW TABLES").fetchdf()
st.write("📋 Tillgängliga tabeller i databasen:", tables)

# Försök läsa data från någon tabell som finns
try:
    df = con.execute("""
        SELECT occupation AS Yrkesområde,
               municipality AS Kommun,
               COUNT(*) AS Antal_annons
        FROM job_ads_dataset.job_ads_hr
        GROUP BY occupation, municipality
        ORDER BY Antal_annons DESC
    """).fetchdf()

    st.subheader("Antal jobbannonser per kommun och yrkesområde")
    st.bar_chart(df.set_index("Kommun"))

    st.subheader("Detaljerad tabell")
    st.dataframe(df)

except Exception as e:
    st.error(f"Fel vid laddning av data: {e}")


#streamlit run dashboard.py

