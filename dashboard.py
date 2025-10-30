import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime


st.set_page_config(page_title="JobTech Realtime Dashboard", layout="wide")


st.markdown("""
    <style>
    .block-container {padding-top: 1rem;}
    h1, h2, h3 {color: #F4F4F4;}
    body {background-color: #0E1117; color: #E0E0E0;}
    </style>
""", unsafe_allow_html=True)

st.title("JobTech Realtime Dashboard")
st.caption("Visar färska jobbannonser direkt från JobTech API (realtid)")


def fetch_jobs(keywords):
    url = "https://jobsearch.api.jobtechdev.se/search"
    all_jobs = []
    headers = {"accept": "application/json"}
    for k in keywords:
        params = {"q": k, "limit": 100}  
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            hits = data.get("hits", [])
            for ad in hits:
                workplace = ad.get("workplace_address", {})
                all_jobs.append({
                    "Titel": ad.get("headline"),
                    "Arbetsgivare": ad.get("employer", {}).get("name"),
                    "Kommun": workplace.get("municipality"),
                    "Yrkesområde": k
                })
        except Exception as e:
            st.error(f"Kunde inte hämta data för '{k}': {e}")
    return pd.DataFrame(all_jobs)


if st.button("Hämta ny data (realtid)"):
    st.info("Hämtar färska jobbannonser...")
    df = fetch_jobs(["data", "hr", "ekonomi"])
    if df.empty:
        st.warning("Inga jobbannonser hittades.")
    else:
        st.session_state["jobs_df"] = df
        st.success(f"{len(df)} annonser hämtades ({datetime.now().strftime('%H:%M:%S')})")


if "jobs_df" in st.session_state and not st.session_state["jobs_df"].empty:
    df = st.session_state["jobs_df"]

    # 1
    st.subheader("1. Fördelning per yrkesområde")
    fig1 = px.bar(
        df.groupby("Yrkesområde").size().reset_index(name="Antal"),
        x="Yrkesområde", y="Antal", color="Yrkesområde",
        text="Antal", title="Antal jobb per yrkesområde", template="plotly_dark"
    )
    fig1.update_traces(textposition='outside')
    st.plotly_chart(fig1, use_container_width=True)

    # 2
    st.subheader("2. Topp 10 kommuner med flest jobb")
    kommun_df = df["Kommun"].value_counts().head(10).reset_index()
    kommun_df.columns = ["Kommun", "Antal"]
    fig2 = px.bar(
        kommun_df, x="Kommun", y="Antal", color="Kommun",
        text="Antal", title="Kommuner med flest lediga jobb", template="plotly_dark"
    )
    fig2.update_traces(textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)

    # 3
    st.subheader("3. Största arbetsgivare")
    employer_df = df["Arbetsgivare"].value_counts().head(10).reset_index()
    employer_df.columns = ["Arbetsgivare", "Antal"]
    fig3 = px.bar(
        employer_df, y="Arbetsgivare", x="Antal", orientation="h",
        text="Antal", title="Topp 10 största arbetsgivare", template="plotly_dark",
        color="Antal", color_continuous_scale="Blues"
    )
    fig3.update_traces(textposition='outside')
    st.plotly_chart(fig3, use_container_width=True)

    # 4
    st.subheader("4. Jobb per kommun och yrkesområde (topp 20)")
    combo_df = (
        df.groupby(["Yrkesområde", "Kommun"])
        .size()
        .reset_index(name="Antal")
        .sort_values("Antal", ascending=False)
        .head(20)
    )
    fig4 = px.bar(
        combo_df, x="Kommun", y="Antal", color="Yrkesområde",
        title="Topp 20 kombinationer av kommun & yrkesområde", template="plotly_dark"
    )
    st.plotly_chart(fig4, use_container_width=True)

    
    st.subheader("5. Rådata (senaste hämtningen)")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Tryck på 'Hämta ny data (realtid)' för att ladda in färska jobbannonser.")
