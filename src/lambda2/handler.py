import boto3


def handler(event, context):
    # Fetch the raw data file triggered by S3 event
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=event["bucket"], Key=event["key"])
    payload = obj["Body"].read().decode()

    # Write parsed records to DynamoDB
    dynamodb = boto3.client("dynamodb")
    dynamodb.batch_write_item(
        RequestItems={
            "processed-events": [
                {"PutRequest": {"Item": {"pk": {"S": event["id"]}, "data": {"S": payload}}}}
            ]
        }
    )

    # Publish notification to SNS topic
    sns = boto3.client("sns")
    sns.publish(TopicArn=event["topic_arn"], Message=f"Processed {event['id']}")

    # Trigger downstream processing lambda
    lam = boto3.client("lambda")
    lam.invoke(FunctionName="downstream-processor", Payload=payload.encode())

    return {"records_processed": 1}
