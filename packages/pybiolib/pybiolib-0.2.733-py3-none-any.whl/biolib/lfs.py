import os
import requests

from biolib.biolib_api_client.biolib_account_api import BiolibAccountApi
from biolib.biolib_api_client import BiolibApiClient
from biolib.biolib_logging import logger
from biolib.biolib_errors import BioLibError


def create_large_file_system(zip_file_path: str, team_account_handle: str):
    if not BiolibApiClient.api_client or not BiolibApiClient.api_client.is_signed_in:
        raise BioLibError(
            'You must be signed in to create a Large File System, set the environment variable "BIOLIB_TOKEN"'
        )

    if not os.path.exists(zip_file_path):
        raise BioLibError(f"Could not find file at {zip_file_path}")

    account = BiolibAccountApi.fetch_by_handle(team_account_handle)
    lfs = BiolibAccountApi.create_large_file_system(
        account_public_id=account['public_id'],
    )
    presigned_post = lfs['presigned_post']
    files = {'file': (zip_file_path, open(zip_file_path, 'rb'))}

    try:
        logger.info("Uploading...")
        upload_response = requests.post(presigned_post['url'], data=presigned_post['fields'], files=files)
    except Exception as error:
        raise BioLibError(f"Failed to reach out to S3 at url: {presigned_post['url']}") from error

    if not upload_response.ok:
        raise BioLibError(upload_response.content)

    logger.info("Succesfully created a Large File System")
