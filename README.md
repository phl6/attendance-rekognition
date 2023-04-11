# attendance-rekognition

### Introduction
This project utilizes AWS Rekognition to find matching faces with a given photo. 
The ultimate goal is to take attendance in an event by taking photos of attendees by interval(e.g. 1 min) and send it to aws to do matchings.

Whenever a photo is uploaded to s3 bucket, a aws lambda function is triggered, the faceId is then indexed to dynamodb.
Then, when a photo is taken and used to call rekognition api, we are able to retrieve the person's identity, therefore achieving attendance taking functionality.

---

### Initial Setup

1. Install virtualenv in global: ```pip install virtualenv```

2. Activate existing venv: ```source ./venv/bin/activate```

3. Install dependencies: ```pip install -r requirement.txt```

4. Set up aws connection: ```aws configure``` ([generate AWS access key](https://us-east-1.console.aws.amazon.com/iamv2/home#/security_credentials))

5. Deactivate virtualenv: ```deactivate```

---

### AWS Setup
1. Create S3 Bucket <bucket-name> with <region-name>
```shell
# Syntax:
$ aws s3api create-bucket --bucket <bucket-name> \
--region <region-name> \
--create-bucket-configuration \
LocationConstraint=<region-name>

# Example:
$ aws s3api create-bucket --bucket attendance-records \
--region ap-southeast-1 \
--create-bucket-configuration \
LocationConstraint=ap-southeast-1
```

Result: 
![s3CreationResult](https://user-images.githubusercontent.com/43781029/231078683-69f66ae8-4997-44aa-babf-214eb4b0c975.png)

2. Create Rekognition collection <collection-name>
```shell
# Syntax:
$ aws rekognition create-collection --collection-id <collection-name> --region <region-name>

# Example:
$ aws rekognition create-collection --collection-id analystFaces_collection --region ap-southeast-1
```
Result: 
![rekognitionCreationResult](https://user-images.githubusercontent.com/43781029/231079097-0755942e-0f8e-4604-bcd3-59668d059ab2.png)

3. Create table and index in DynamoDB with <table-name>
```shell
# Syntax:
$ aws dynamodb create-table --table-name <table-name> \
--attribute-definitions AttributeName=<attribute-name>, AttributeType=S \
--key-schema AttributeName=<attribute-name>, KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1, WriteCapacityUnits=1 \
--region <region-name>

# Example:
$ aws dynamodb create-table --table-name analystFaces \
--attribute-definitions AttributeName=FaceId, AttributeType=S \
--key-schema AttributeName=FaceId, KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1, WriteCapacityUnits=1 \
--region ap-southeast-1
```
  
---
  
### Resources
[AWS Reference](https://aws.amazon.com/blogs/machine-learning/build-your-own-face-recognition-service-using-amazon-rekognition/)<br>
[DynamoDB Reference](https://blog.awsfundamentals.com/aws-dynamodb-data-types)<br>
[Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/head_object.html)<br>


