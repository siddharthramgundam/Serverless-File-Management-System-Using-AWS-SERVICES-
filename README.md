
**Step-by-Step Guide to Build a Serverless File Management System**

**Project Description**

The Serverless File Management System automates the process of handling file uploads in the cloud. Whenever a user uploads a file to an Amazon S3 bucket, an AWS Lambda function is automatically triggered. This function extracts file metadata (such as file name, size, and upload time) and stores it in Amazon DynamoDB for tracking and analysis. Optionally, an email notification can be sent using Amazon SNS.

This project demonstrates a serverless cloud architecture — no servers to manage, only managed services.



**Use Cases**
Here’s your professionally formatted, bold, and polished version of the guide without emojis — perfect for documentation, resume attachment, or portfolio presentation:



Step-by-Step Guide to Build a Serverless File Management System

**Project Description**

The Serverless File Management System automates the process of handling file uploads in the cloud. Whenever a user uploads a file to an Amazon S3 bucket, an AWS Lambda function is automatically triggered. This function extracts file metadata (such as file name, size, and upload time) and stores it in Amazon DynamoDB for tracking and analysis. Optionally, an email notification can be sent using Amazon SNS.

This project demonstrates a serverless cloud architecture — no servers to manage, only managed services.



**Use Cases**

1. Automated File Tracking

Automatically log every file uploaded to cloud storage for auditing, analytics, or compliance purposes.

2. Cloud Backup Management

Store file details upon upload for recovery, version control, or backup validation.

3. Data Processing Pipelines

Trigger downstream data processing (ETL or analytics) whenever a new file is uploaded.

4. Email Notification System

Send real-time notifications to stakeholders whenever new files are uploaded — useful in multi-user or multi-department environments.



**Project Architecture**

Architecture Components

Amazon S3: File storage and event source.

AWS Lambda: Processes file metadata automatically upon upload.

Amazon DynamoDB: Stores metadata (file name, size, upload time).

Amazon SNS (Optional): Sends email alerts upon file upload.

Amazon CloudWatch: Monitors and logs Lambda execution.


Architecture Flow

1. User uploads a file to Amazon S3.


2. S3 triggers the Lambda function.


3. Lambda extracts metadata.


4. Metadata is stored in DynamoDB.


5. (Optional) SNS sends an email notification.


6. Logs are captured and monitored in CloudWatch.





**Step-by-Step Deployment**

Step 1 — Create an S3 Bucket

1. Navigate to AWS Console → S3 → Create Bucket.


2. Enter a name: serverless-file-bucket-sid.


3. Region: ap-south-1.


4. Leave other settings as default and click Create Bucket.






Step 2 — Create DynamoDB Table

1. Go to AWS Console → DynamoDB → Create Table.


2. Table name: FileMetadata.


3. Partition key: FileName (String).


4. Leave default settings and click Create.





Step 3 — Create Lambda Function

1. Go to AWS Lambda → Create Function.


2. Name: FileMetadataHandler.


3. Runtime: Python 3.12.


4. Create a new role with permissions for Lambda, DynamoDB, and SNS.


5. Click Create Function.



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
        message = (
            f"New file uploaded!\n\n"
            f"File: {file_name}\n"
            f"Bucket: {bucket}\n"
            f"Size: {file_size} bytes\n"
            f"Uploaded at: {event_time}"
        )
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

1. In Lambda Function → Configuration → Triggers → Add Trigger.


2. Select S3.


3. Choose bucket: serverless-file-bucket-sid.


4. Event type: All object create events.


5. Enable trigger and click Save.





Step 5 — Create SNS Topic (Optional)

1. Go to Amazon SNS → Create Topic → Standard.


2. Name: file-upload-alerts.


3. Copy the Topic ARN.


4. Subscribe with your email ID and confirm the subscription via email.


5. Replace the SNS_TOPIC_ARN value in the Lambda code with your topic ARN.





Step 6 — Upload a Test File

1. Open your S3 bucket.


2. Click Upload → Add File → Select a file (e.g., Banking.csv).


3. Upload and wait for a few seconds.




Step 7 — Verify Outputs

CloudWatch Logs: Confirm Lambda execution logs.

DynamoDB Table: Verify that a new record has been added.

Email (if SNS used): Check for the upload alert notification.


**Sample CloudWatch Log Output:**

Event received: {"Records": [{"eventSource": "aws:s3", "eventName": "ObjectCreated:Put"}]}
New file uploaded: Banking.csv in bucket: serverless-file-bucket-sid
Metadata stored successfully
SNS notification sent successfully



**Cloud Concepts Demonstrated**

Serverless Architecture: Fully managed, auto-scaling, event-driven system.

Event-Driven Computing: S3 automatically triggers Lambda upon file upload.

NoSQL Data Storage: DynamoDB provides fast, scalable metadata storage.

Monitoring & Observability: CloudWatch captures detailed execution logs.

Decoupled Services: Independent AWS services integrated through events.





**Real-World Application Example**

A Digital Media Company uses this system to automatically log and notify teams whenever new images, videos, or documents are uploaded by contributors.
This ensures centralized metadata tracking, instant notifications, and streamlined workflows — enhancing transparency and eliminating manual tracking.



**Final Outcome**

Automated, secure, and serverless file management pipeline.

Uploading a file triggers Lambda, which stores metadata in DynamoDB and sends optional SNS notifications.

Scalable, event-driven, and production-ready design.





1. Automated File Tracking

Automatically log every file uploaded to cloud storage for auditing, analytics, or compliance purposes.

2. Cloud Backup Management

Store file details upon upload for recovery, version control, or backup validation.

3. Data Processing Pipelines

Trigger downstream data processing (ETL or analytics) whenever a new file is uploaded.

4. Email Notification System

Send real-time notifications to stakeholders whenever new files are uploaded — useful in multi-user or multi-department environments.



**Project Architecture**

**Architecture Components**

Amazon S3: File storage and event source.

AWS Lambda: Processes file metadata automatically upon upload.

Amazon DynamoDB: Stores metadata (file name, size, upload time).

Amazon SNS (Optional): Sends email alerts upon file upload.

Amazon CloudWatch: Monitors and logs Lambda execution.


**Architecture Flow**

1. User uploads a file to Amazon S3.


2. S3 triggers the Lambda function.


3. Lambda extracts metadata.


4. Metadata is stored in DynamoDB.


5. (Optional) SNS sends an email notification.


6. Logs are captured and monitored in CloudWatch.




**Step-by-Step Deployment**

Step 1 — Create an S3 Bucket

1. Navigate to AWS Console → S3 → Create Bucket.


2. Enter a name: serverless-file-bucket-sid.


3. Region: ap-south-1.


4. Leave other settings as default and click Create Bucket.





Step 2 — Create DynamoDB Table

1. Go to AWS Console → DynamoDB → Create Table.


2. Table name: FileMetadata.


3. Partition key: FileName (String).


4. Leave default settings and click Create.




Step 3 — Create Lambda Function

1. Go to AWS Lambda → Create Function.


2. Name: FileMetadataHandler.


3. Runtime: Python 3.12.


4. Create a new role with permissions for Lambda, DynamoDB, and SNS.


5. Click Create Function.



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
        message = (
            f"New file uploaded!\n\n"
            f"File: {file_name}\n"
            f"Bucket: {bucket}\n"
            f"Size: {file_size} bytes\n"
            f"Uploaded at: {event_time}"
        )
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

1. In Lambda Function → Configuration → Triggers → Add Trigger.


2. Select S3.


3. Choose bucket: serverless-file-bucket-sid.


4. Event type: All object create events.


5. Enable trigger and click Save.





Step 5 — Create SNS Topic (Optional)

1. Go to Amazon SNS → Create Topic → Standard.


2. Name: file-upload-alerts.


3. Copy the Topic ARN.


4. Subscribe with your email ID and confirm the subscription via email.


5. Replace the SNS_TOPIC_ARN value in the Lambda code with your topic ARN.




Step 6 — Upload a Test File

1. Open your S3 bucket.


2. Click Upload → Add File → Select a file (e.g., Banking.csv).


3. Upload and wait for a few seconds.






Step 7 — Verify Outputs

CloudWatch Logs: Confirm Lambda execution logs.

DynamoDB Table: Verify that a new record has been added.

Email (if SNS used): Check for the upload alert notification.


**Sample CloudWatch Log Output:**

Event received: {"Records": [{"eventSource": "aws:s3", "eventName": "ObjectCreated:Put"}]}
New file uploaded: Banking.csv in bucket: serverless-file-bucket-sid
Metadata stored successfully
SNS notification sent successfully



**Cloud Concepts Demonstrated**

Serverless Architecture: Fully managed, auto-scaling, event-driven system.

Event-Driven Computing: S3 automatically triggers Lambda upon file upload.

NoSQL Data Storage: DynamoDB provides fast, scalable metadata storage.

Monitoring & Observability: CloudWatch captures detailed execution logs.

Decoupled Services: Independent AWS services integrated through events.




**Real-World Application Example**

A Digital Media Company uses this system to automatically log and notify teams whenever new images, videos, or documents are uploaded by contributors.
This ensures centralized metadata tracking, instant notifications, and streamlined workflows — enhancing transparency and eliminating manual tracking.




Final Outcome

Automated, secure, and serverless file management pipeline.

Uploading a file triggers Lambda, which stores metadata in DynamoDB and sends optional SNS notifications.

Scalable, event-driven, and production-ready design.


?
