from azure.storage.blob import BlobClient, ContainerClient
import os

def download_duckdb_from_blob(conn_str, container_name, blob_name, local_path):
    blob = BlobClient.from_connection_string(conn_str, container_name, blob_name)
    with open(local_path, "wb") as f:
        stream = blob.download_blob()
        stream.readinto(f)

def upload_duckdb_to_blob(conn_str, container_name, blob_name, local_path):
    blob = BlobClient.from_connection_string(conn_str, container_name, blob_name)
    with open(local_path, "rb") as f:
        blob.upload_blob(f, overwrite=True)
