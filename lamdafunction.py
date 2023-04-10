import boto3

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

BUCKET_NAME = 'analyst-photos'
DYNAMO_TABLE_NAME = 'analystFaces'
REKOGNITION_COLLECTION_ID = 'analystFaces_collection'


# --------------- Helper Functions ------------------

def index_faces(bucket, key):
    return rekognition.index_faces(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key
            }
        }, CollectionId = REKOGNITION_COLLECTION_ID)
    
def update_index(tableName, faceId, fullName):
    return dynamodb.put_item(
        TableName=tableName,
        Item={
            'FaceId': {'S': faceId},
            'FullName': {'S': fullName}
            }
        ) 
    
# --------------- Main handler ------------------

def lambda_handler(event, context):
    print("Event:" + str(event))
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    print("bucket: " + bucket)
    key = event['Records'][0]['s3']['object']['key']

    try:
        # Calls Amazon Rekognition IndexFaces API to detect faces in S3 object 
        # to index faces into specified collection
        response = index_faces(BUCKET_NAME, key)
        print("Response1: " + str(response))
        
        # Commit faceId and full name object metadata to DynamoDB
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']
            print("faceId: " + str(faceId))

            ret = s3.head_object(Bucket=bucket, Key=key)
            print("ret: " + str(ret))
            print("Metadata: " + str(ret['Metadata']))
            personFullName = ret['Metadata']['fullname']

            dynamoUpdateResult = update_index(DYNAMO_TABLE_NAME, faceId, personFullName)
            print("dynamoUpdateResult" + str(dynamoUpdateResult))
            
        # Print response to console
        print("Response2: " + str(response))

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket))
        raise e