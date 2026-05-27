import boto3


def handler(event, context):
    # Store the incoming event
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(event["table_name"])
    table.put_item(Item=event["record"])

    # Upload a report to S3
    s3 = boto3.client("s3")
    s3.put_object(Bucket=event["bucket"], Key=f"reports/{event['id']}.json", Body=event["data"].encode())

    # Read credentials for downstream call
    client = boto3.client("secretsmanager")
    secret = client.get_secret_value(SecretId="my-app/api-key")

    # Notify downstream
    sqs = boto3.client("sqs")
    sqs.send_message(QueueUrl=event["queue_url"], MessageBody=f"processed {event['id']}")

    # Clean up old artifacts
    s3.delete_object(Bucket=event["bucket"], Key=f"staging/{event['id']}.tmp")

    return {"status": "ok", "api_key": secret["SecretString"]}
