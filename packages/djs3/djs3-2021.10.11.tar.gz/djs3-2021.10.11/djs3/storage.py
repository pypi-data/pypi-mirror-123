from typing import TextIO

from django.core.files.storage import Storage

from .s3 import S3, NoSuchKey


class S3Storage(Storage):
    def __init__(self):
        self.s3 = S3()

    def _open(self, name: str, mode="rb"):
        data, metadata = self.s3.get(name)
        return data

    def _save(self, name: str, content: TextIO):
        self.s3.upload_file(content, name)

    def exists(self, name: str):
        try:
            data, metadata = self.s3.get(name)
            return True
        except NoSuchKey:
            return False

    def delete(self, name: str):
        self.s3.delete(name)

    def url(self, name):
        return (
            self.s3.settings.aws_s3_endpoint_url
            + "/"
            + self.s3.settings.aws_s3_bucket_name
            + "/"
            + name
        )


class S3StaticStorage(S3Storage):
    pass
