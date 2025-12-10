

# Step-by-Step Guide to Build a Serverless File Management System

## Project Description:

The Serverless File Management System automates the process of handling file uploads in the cloud. Whenever a user uploads a file to an Amazon S3 bucket, an AWS Lambda function is automatically triggered. This Lambda function extracts file metadata (like file name, size, and upload time) and stores it in Amazon DynamoDB for tracking and analysis. Optionally, an email notification is sent using Amazon SNS.

This project demonstrates a serverless cloud architecture — no servers to manage, only managed services.

-Use Cases

1. Automated File Tracking:
Companies can automatically log every file uploaded to cloud storage — useful for auditing, analytics, or compliance.


2. Cloud Backup Management:
Whenever files are uploaded to an S3 bucket, their details are stored for recovery or version control purposes.


3. Data Processing Pipelines:
Lambda triggers can initiate ETL jobs or downstream data pipelines (e.g., notifying a data analytics system).


4. Email Notification System:
Using SNS, stakeholders get notified when new files are uploaded — helpful in multi-user or multi-department environments.


## Project Architecture

Architecture Components:

Amazon S3 — File storage and event source.

AWS Lambda — Processes metadata automatically upon file upload.

Amazon DynamoDB — Stores metadata (file name, size, upload time).

Amazon SNS (optional) — Sends email alerts for each new upload.

Amazon CloudWatch — Monitors logs for Lambda executions.


Architecture Block Diagram:-

![WhatsApp Image 2025-12-10 at 19 25 35_87de039c](https://github.com/user-attachments/assets/fcf3a294-0865-4f91-a154-39a2d3324004)


## Step-by-Step Deployment

Step 1 — Create an S3 Bucket

Go to AWS Console → S3 → Create Bucket

Name: serverless-file-bucket-sid

Region: ap-south-1

Leave default settings → click Create Bucket




Step 2 — Create DynamoDB Table

Go to AWS Console → DynamoDB → Create Table

Table name: FileMetadata

Partition key: FileName (String)

Keep default settings → click Create




Step 3 — Create Lambda Function

Go to AWS Lambda → Create Function

Name: FileMetadataHandler

Runtime: Python 3.12

Create new role with basic Lambda + DynamoDB + SNS permissions

Click Create Function


Add the following Python code:

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



Step 4 — Add S3 Trigger

In Lambda function → Configuration → Triggers → Add trigger

Select S3

Choose bucket: serverless-file-bucket-sid

Event type: All object create events

Enable trigger → Save




Step 5 — Create SNS Topic

Go to SNS → Create Topic → Standard

Name: file-upload-alerts

Copy the Topic ARN

Subscribe with your email ID → confirm the subscription via email.

Replace ARN in the Lambda code (SNS_TOPIC_ARN value).




Step 6 — Upload Test File

Go to your S3 bucket

Click Upload → Add file → Banking.csv (or any file)

Upload it and wait a few seconds



Step 7 — Verify Outputs

✅ Go to CloudWatch Logs → check Lambda execution logs
✅ Go to DynamoDB Table → confirm new record added
✅ Check email inbox (if SNS added) → see upload alert



## Sample Output Log (CloudWatch)

Event received: {"Records": [{"eventSource": "aws:s3", "eventName": "ObjectCreated:Put"}]}
New file uploaded: Banking.csv in bucket: serverless-file-bucket-sid
Metadata stored successfully
SNS notification sent successfully!



## Cloud Concepts Demonstrated

Serverless Architecture — Fully managed, auto-scaling, event-driven.

Event-driven Computing — S3 triggers Lambda automatically.

NoSQL Data Storage — DynamoDB used for fast metadata storage.

Monitoring & Observability — CloudWatch logs show Lambda execution.

Decoupled Services — Each AWS service operates independently yet integrates seamlessly.




## Real-World Application Example

A Digital Media Company uses this setup to automatically log and notify teams whenever new images, videos, or reports are uploaded by photographers or content creators.
This ensures automated tracking, centralized metadata management, and instant alerts, improving workflow transparency and reducing manual tracking.



## Final Outcome

 Automated, secure, and serverless file management pipeline.
 Upload a file → triggers Lambda → stores metadata → sends email.
 Scalable, event-driven, and production-ready design
