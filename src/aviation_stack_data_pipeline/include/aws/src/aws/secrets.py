import boto3


class Secrets:
    def __init__(self):
        self.client = boto3.client("secretsmanager")

    def get(self, secret_name: str) -> str:
        return self.client.get_secret_value(SecretId=secret_name)
