import mimetypes
from typing import Tuple, Dict, TextIO

import boto3
from botocore.exceptions import ClientError
from pydantic import BaseSettings


class Settings(BaseSettings):
    aws_region: str = "eu-west-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_session_token: str = ""
    aws_s3_bucket_name: str = ""
    aws_s3_endpoint_url: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class NoSuchKey(Exception):
    def __init__(self, key, bucket):
        self.key = key
        self.bucket = bucket
        self.message = f"No object in bucket {bucket} matches {key}. Has it expired?"
        super().__init__(self.message, self.bucket)


class NoSuchBucket(Exception):
    def __init__(self, bucket_name):
        self.bucket = bucket_name
        self.message = f"Bucket {bucket_name} does not exist!"
        super().__init__(self.message, self.bucket)


class BucketAccessDenied(Exception):
    def __init__(self, bucket_name):
        self.bucket = bucket_name
        self.message = f"Unable to access bucket {self.bucket}. Does it exist?"

        super().__init__(self.message, self.bucket)


class UnknownBucketException(Exception):
    def __init__(self, bucket_name, e: ClientError):
        self.bucket = bucket_name
        error_code: str = e.response.get("Error").get("Code")
        error_message: str = e.response.get("Error").get("Message")
        self.message = f"Unknown Bucket Exception {error_code}: {error_message}"
        super().__init__(self.message, self.bucket)


class S3:
    def _get_resource(self):
        _session = boto3.Session(
            aws_access_key_id=self.settings.aws_access_key_id,
            aws_secret_access_key=self.settings.aws_secret_access_key,
            aws_session_token=self.settings.aws_session_token,
            region_name=self.settings.aws_region,
        )
        resource = _session.resource(
            service_name="s3", endpoint_url=self.settings.aws_s3_endpoint_url
        )
        return resource

    def __init__(self):
        self.settings = Settings()
        self.resource = self._get_resource()

    def _handle_boto3_client_error(self, e: ClientError, key=None):
        error_code: str = e.response.get("Error").get("Code")
        if error_code == "AccessDenied":
            raise BucketAccessDenied(self.settings.aws_s3_bucket_name)
        elif error_code == "NoSuchBucket":
            raise NoSuchBucket(self.settings.aws_s3_bucket_name)
        elif error_code == "NoSuchKey":
            raise NoSuchKey(key, self.settings.aws_s3_bucket_name)
        else:
            raise UnknownBucketException(self.settings.aws_s3_bucket_name, e)

    def get(self, key: str, response_content_type: str = None) -> Tuple[bytes, Dict]:
        s3_bucket = self.resource.Object(self.settings.aws_s3_bucket_name, key)
        try:
            if response_content_type:
                response = s3_bucket.get(ResponseContentType=response_content_type)
            else:
                response = s3_bucket.get()
            data = response.get("Body").read()
            metadata: Dict = response.get("Metadata")
            return data, metadata
        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

    def upload_file(self, data: TextIO, key: str) -> Dict:
        s3_bucket = self.resource.Object(self.settings.aws_s3_bucket_name, key)
        mimetype, _ = mimetypes.guess_type(key)
        if mimetype is None:
            mimetype = "binary/octet-stream"
        try:
            response = s3_bucket.meta.client.upload_fileobj(
                data, self.settings.aws_s3_bucket_name, key, {"ContentType": mimetype}
            )
            return response
        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

    def delete(self, key: str) -> Dict:
        s3_bucket = self.resource.Object(self.settings.aws_s3_bucket_name, key)
        try:
            response = s3_bucket.delete()
            return response
        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)
