from datetime import datetime, timedelta
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import gzip
import json
import os

# Environment/config variables (replace with your own or use env vars)
COSMOS_URI = os.environ["COSMOS_URI"]
COSMOS_KEY = os.environ["COSMOS_KEY"]
DB_NAME = os.environ["DB_NAME"]
COLLECTION_NAME = os.environ["COLLECTION_NAME"]
BLOB_CONN_STR = os.environ["BLOB_CONN_STR"]
CONTAINER_NAME = os.environ.get("BLOB_CONTAINER", "billing-archive")

cosmos_client = CosmosClient(COSMOS_URI, COSMOS_KEY)
db = cosmos_client.get_database_client(DB_NAME)
container = db.get_container_client(COLLECTION_NAME)
blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
blob_container = blob_service.get_container_client(CONTAINER_NAME)

def archive_old_records():
    cutoff = (datetime.utcnow() - timedelta(days=90)).isoformat()
    query = "SELECT * FROM c WHERE c.createdAt < @cutoff"
    params = [{"name": "@cutoff", "value": cutoff}]
    old_records = list(container.query_items(query, parameters=params, enable_cross_partition_query=True))
    batch_size = 1000
    for i in range(0, len(old_records), batch_size):
        batch = old_records[i:i+batch_size]
        data = json.dumps(batch)
        data_gz = gzip.compress(data.encode("utf-8"))
        blob_name = f"archive_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{i}.json.gz"
        blob_container.upload_blob(blob_name, data_gz, overwrite=True)
        for record in batch:
            container.delete_item(record['id'], partition_key=record['partitionKey'])
