import boto3
import io
from PIL import Image

DYNAMO_TABLE_NAME = "analystFaces"
REKOGNITION_COLLECTION_ID = "analystFaces_collection"
REGION = "ap-southeast-1"
MAX_FACES = 20

rekognition = boto3.client("rekognition", REGION)
dynamodb = boto3.client("dynamodb", REGION)
    
image = Image.open("./resources/3Faces.jpg")
stream = io.BytesIO()
image.save(stream, format = "JPEG")
image_binary = stream.getvalue()

try:
    # plot faces in photo and return FaceId (defined in dynamodb)
    response = rekognition.search_faces_by_image(
            CollectionId = REKOGNITION_COLLECTION_ID,
            Image = {'Bytes': image_binary},
            MaxFaces = MAX_FACES                     
        )
    print("response1: " + str(response['FaceMatches']))
    print("Total matched faces: " + str(len(response['FaceMatches'])))
    print("-------------------------------------------------------------")
    print("Total search face confidence level: " + str(response["SearchedFaceConfidence"]))
    print("-------------------------------------------------------------")

    # print out results
    for index, match in enumerate(response['FaceMatches']):
        # find person by faceId(index) in dynamodb
        face = dynamodb.get_item(
            TableName = DYNAMO_TABLE_NAME,  
            Key={'FaceId': {'S': match['Face']['FaceId']}}
        )
        
        if 'Item' in face:
            print ("Face " + str(index) + " is recognized as : " + face['Item']['FullName']['S'])
        else:
            print ("Face " + str(index) + " is recognized as : " + "no match")
            
        print ("Details: " + match['Face']['FaceId'], match['Face']['Confidence'])
        print("-------------------------------------------------------------")
except rekognition.exceptions.InvalidParameterException:
    print("-------------------------------------------------------------")
    print("No Faces Found")
    print("-------------------------------------------------------------")