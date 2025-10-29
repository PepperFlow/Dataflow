import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# 
st.set_page_config(page_title="DataFlow Dashboard", layout="wide")

# mörkt tema
st.markdown("""
    <style>
    .block-container {padding-top: 1rem;}
    h1, h2, h3 {color: #F4F4F4;}
    body {background-color: #0E1117; color: #E0E0E0;}
    </style>
""", unsafe_allow_html=True)

st.title("JobTech Analytics Dashboard")
st.caption("Visualisering av jobbdata från JobTech API by DataFlow Team")

# Databas
try:
    con = duckdb.connect("job_ads_pipeline.duckdb", read_only=True)
except Exception as e:
    st.error(f"Kunde inte ansluta till DuckDB: {e}")
    st.stop()

# 1
st.subheader("1. Fördelning per yrkesområde")
query1 = """
SELECT occupation_field AS yrkesområde, COUNT(*) AS antal
FROM main.stg_job_ads
GROUP BY occupation_field
ORDER BY antal DESC
"""
df1 = con.execute(query1).fetchdf()
fig1 = px.bar(
    df1,
    x='yrkesområde',
    y='antal',
    text='antal',
    color='yrkesområde',
    title='Antal jobb per yrkesområde',
    template='plotly_dark'
)
fig1.update_traces(textposition='outside')
st.plotly_chart(fig1, use_container_width=True)

# 2
# ==== VISUALISERING 2 ====
st.subheader("2. Topp 10 kommuner med flest jobb")
query2 = """
SELECT municipality AS kommun, COUNT(*) AS antal
FROM main.stg_job_ads
WHERE municipality IS NOT NULL
GROUP BY municipality
ORDER BY antal DESC
LIMIT 10
"""
df2 = con.execute(query2).fetchdf()
fig2 = px.bar(
    df2,
    x='kommun',
    y='antal',
    color='kommun',
    text='antal',
    title='Kommuner med flest lediga jobb',
    template='plotly_dark'
)
fig2.update_traces(textposition='outside')
st.plotly_chart(fig2, use_container_width=True)


# 3
st.subheader("3. Största arbetsgivarna")
query3 = """
SELECT employer, COUNT(*) as antal_annonser
FROM main.stg_job_ads
WHERE employer IS NOT NULL
GROUP BY employer
ORDER BY antal_annonser DESC
LIMIT 10
"""
df3 = con.execute(query3).fetchdf()
fig3 = px.bar(
    df3,
    y='employer',
    x='antal_annonser',
    orientation='h',
    text='antal_annonser',
    title='Top 10 största arbetsgivarna',
    template='plotly_dark',
    color='antal_annonser',
    color_continuous_scale='Blues'
)
fig3.update_traces(textposition='outside')
st.plotly_chart(fig3, use_container_width=True)

# 4
st.subheader("4. Jobb per kommun och yrkesområde (topp 20)")
query4 = """
SELECT 
    occupation_field as Yrkesområde,
    municipality as Kommun,
    COUNT(*) as Antal
FROM main.stg_job_ads
WHERE municipality IS NOT NULL
GROUP BY occupation_field, municipality
ORDER BY Antal DESC
LIMIT 20
"""
df4 = con.execute(query4).fetchdf()
fig4 = px.bar(
    df4,
    x='Kommun',
    y='Antal',
    color='Yrkesområde',
    title='Topp 20 kombinationer av kommun & yrkesområde',
    template='plotly_dark'
)
st.plotly_chart(fig4, use_container_width=True)

# ANSLUTNING 
con.close()

st.markdown("---")

