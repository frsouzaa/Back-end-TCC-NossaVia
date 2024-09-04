import base64
from azure.storage.blob import BlobServiceClient
from os import getenv


def upload_blob(base64_string: str, blob_name: str):
    connection_string = getenv("AZURE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = getenv("AZURE_BLOB_CONTAINER")

    image_data = base64.b64decode(base64_string)

    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    blob_client.upload_blob(image_data, blob_type="BlockBlob")
