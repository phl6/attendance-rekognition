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
    key = event['Records'][0]['s3']['object']['key']

    try:
        # to index faces into specified collection
        response = index_faces(BUCKET_NAME, key)
        print("Response: " + str(response))
        
        # Commit faceId and full name object metadata to DynamoDB
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']

            result = s3.head_object(Bucket=bucket, Key=key)
            print("result: " + str(result))
            personFullName = result['Metadata']['fullname']

            # update dynamodb index
            dynamoUpdateResult = update_index(DYNAMO_TABLE_NAME, faceId, personFullName)
            print("dynamoUpdateResult" + str(dynamoUpdateResult))

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket))
        raise e