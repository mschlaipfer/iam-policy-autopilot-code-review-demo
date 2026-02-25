import boto3


def upload_file_to_s3(bucket_name: str, file_path: str, object_key: str) -> None:
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket_name, object_key)
    print(f"Uploaded {file_path} to s3://{bucket_name}/{object_key}")


def read_secret(secret_name: str) -> str:
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return response["SecretString"]


def put_item_to_dynamodb(table_name: str, item: dict) -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.put_item(Item=item)
    print(f"Inserted item into DynamoDB table: {table_name}")


def send_sqs_message(queue_url: str, message_body: str) -> None:
    sqs = boto3.client("sqs")
    sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
    print(f"Sent message to SQS queue: {queue_url}")


if __name__ == "__main__":
    upload_file_to_s3("my-bucket", "data.csv", "uploads/data.csv")
    secret = read_secret("my-app/db-password")
    put_item_to_dynamodb("my-table", {"id": "1", "value": "hello"})
    send_sqs_message("https://sqs.us-east-1.amazonaws.com/123456789012/my-queue", "Hello!")
