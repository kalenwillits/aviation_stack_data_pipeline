import io
import boto3


class S3:
    def __init__(self):
        self.client = boto3.client("s3")

    def put(self, bucket: str, key: str, data: bytes):
        self.client.put_object(
            Body=data,
            Bucket=bucket,
            Key=key,
        )

    def get(self, bucket: str, key: str) -> bytes:
        bytes_buffer = io.BytesIO()
        self.client.download_fileobj(Bucket=bucket, Key=key, Fileobj=bytes_buffer)
