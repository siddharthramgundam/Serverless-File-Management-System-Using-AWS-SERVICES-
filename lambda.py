import boto3
import json

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

TABLE_NAME = 'FileMetadata'
SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:YOUR_ACCOUNT_ID:file-upload-alerts'

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        file_name = record['s3']['object']['key']
        file_size = record['s3']['object']['size']
        event_time = record['eventTime']
        
        # Store metadata in DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        response = table.put_item(
            Item={
                'FileName': file_name,
                'BucketName': bucket,
                'FileSize': file_size,
                'UploadTime': event_time
            }
        )
        print("Metadata stored successfully:", response)
        
        # Send SNS Notification
        message = f"📂 New file uploaded!\n\nFile: {file_name}\nBucket: {bucket}\nSize: {file_size} bytes\nUploaded at: {event_time}"
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="New File Upload Alert"
        )
        print("SNS notification sent successfully!")

    return {
        'statusCode': 200,
        'body': json.dumps('File processed successfully!')
    }
