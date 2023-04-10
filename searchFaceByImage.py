import boto3
import io
from PIL import Image

rekognition = boto3.client('rekognition')
dynamodb = boto3.client('dynamodb')

DYNAMO_TABLE_NAME = 'analystFaces'
REKOGNITION_COLLECTION_ID = 'analystFaces_collection'
    
image = Image.open("test.jpeg")
stream = io.BytesIO()
image.save(stream,format="JPEG")
image_binary = stream.getvalue()

# plot faces in photo and return FaceId (defined in dynamodb)
response = rekognition.search_faces_by_image(
        CollectionId = REKOGNITION_COLLECTION_ID,
        Image={'Bytes':image_binary}                                       
        )
# print("response: " + str(response))

# print out results
for match in response['FaceMatches']:
    print (match['Face']['FaceId'], match['Face']['Confidence'])
        
    # match with faceId(index) in dynamodb
    face = dynamodb.get_item(
        TableName = DYNAMO_TABLE_NAME,  
        Key={'FaceId': {'S': match['Face']['FaceId']}}
        )
    print("matching result: " + str(face))
    
    if 'Item' in face:
        print (face['Item']['FullName']['S'])
    else:
        print ('no match found in person lookup')