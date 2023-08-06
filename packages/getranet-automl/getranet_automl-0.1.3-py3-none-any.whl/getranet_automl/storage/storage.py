from starlette.datastructures import UploadFile
from google.cloud import storage


def upload_blob(bucket_name: str, file: UploadFile,
                destination_blob_name: str) -> bool:
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file)

    return 'gs://' + bucket_name + '/' + destination_blob_name


def delete_blob(bucket_name: str, blob_name: str) -> bool:
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    return True
