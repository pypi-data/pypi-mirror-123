from azure.storage.blob import BlobServiceClient, generate_blob_sas, AccountSasPermissions, BlobClient


class BlobService:
    """
    Defines methods for Azure Blob Storage access.
    """
    def __init__(self):
        self.service = None
        self.connection_string = None

    def set_sas(self, connection_string):
        self.connection_string = connection_string
        self.service = BlobServiceClient.from_connection_string(
            connection_string)

    def get_specific_blob_client(self, conn_str, container_name, blob_name):
        return BlobClient.from_connection_string(self,
                                                 conn_str=conn_str,
                                                 container_name=container_name,
                                                 blob_name=blob_name)

    def upload(self, file_path, shared_storage_container, blob_name):
        blob_client = self.service.get_blob_client(
            container=shared_storage_container, blob=blob_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)

    def download(self, tempfile, shared_storage_container, blob_name):
        blob_client = self.service.get_blob_client(
            container=shared_storage_container, blob=blob_name)

        with open(tempfile.file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        return tempfile

    def generate_download_link(self, blob_name, account_name, container_name,
                               account_key, expiry_date):

        url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
        sas_token = generate_blob_sas(
            account_name=account_name,
            account_key=account_key,
            container_name=container_name,
            blob_name=blob_name,
            permission=AccountSasPermissions(read=True),
            expiry=expiry_date)

        return f"{url}?{sas_token}"

    def check_does_blob_exist(self, conn_str, blob_name, container_name):
        blob = self.get_specific_blob_client(self,
                                             conn_str=conn_str,
                                             container_name=container_name,
                                             blob_name=blob_name)
        return blob.exists()

    def delete_blob(self,
                    conn_str,
                    blob_name,
                    container_name,
                    delete_snapshots="include"):
        blob = self.get_specific_blob_client(self,
                                             conn_str=conn_str,
                                             container_name=container_name,
                                             blob_name=blob_name)
        blob.delete_blob(delete_snapshots=delete_snapshots)

    @staticmethod
    def create_anonymous(azure_storage_connection_string):
        blob_service = BlobService()
        blob_service.set_sas(azure_storage_connection_string)
        return blob_service
