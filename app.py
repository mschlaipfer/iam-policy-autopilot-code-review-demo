import boto3


def store_record(table_name: str, item: dict) -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.put_item(Item=item)


def upload_report(bucket: str, key: str, data: bytes) -> None:
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=data)


def read_secret(name: str) -> str:
    client = boto3.client("secretsmanager")
    return client.get_secret_value(SecretId=name)["SecretString"]


def notify(queue_url: str, message: str) -> None:
    sqs = boto3.client("sqs")
    sqs.send_message(QueueUrl=queue_url, MessageBody=message)


def cleanup(bucket: str, key: str) -> None:
    s3 = boto3.client("s3")
    s3.delete_object(Bucket=bucket, Key=key)
