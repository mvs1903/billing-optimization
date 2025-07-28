import gzip
import json

def get_billing_record(record_id):
    record = cosmosdb_get(record_id)
    if record:
        return record
    for blob in list_blobs(CONTAINER_NAME):
        blob_data = download_blob(blob)
        records = json.loads(gzip.decompress(blob_data).decode("utf-8"))
        for r in records:
            if r["id"] == record_id:
                return r
    return None  # Not found

# Helper functions cosmosdb_get, list_blobs, download_blob should wrap respective Azure SDK methods
