# Azure deploy (kort)

- Miljö: **Azure Container Apps** (West Europe)
- ACR: bygg image lokalt för linux/amd64 och pusha
- DuckDB: monterad via Azure Files på `/mnt/duckdb/job_ads.duckdb`
- Viktigt: committa aldrig nycklar, lösenord eller .duckdb-filer

## Snabbkommandon
# bygg & push
docker buildx build --platform linux/amd64 -t <ACR>.azurecr.io/streamlit:latest --push .

# uppdatera app-imagen
az containerapp update -g <RG> -n streamlit-app --image <ACR>.azurecr.io/streamlit:latest
