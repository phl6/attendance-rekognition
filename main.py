import cv2
import time
import boto3
import io
from PIL import Image
from botocore.exceptions import ClientError
import base64


def takePhoto(photoPath):
    # take photo
    result, photo = camera.read()
    # save photo
    cv2.imwrite(photoPath, photo)
    return photo

def convertImageToBytes(photoPath):
    image = Image.open(photoPath)
    image.save(stream, format = "JPEG")
    return stream.getvalue()

def search_faces_by_image(collectionId, image_binary, maxFaces):
    return rekognition.search_faces_by_image(
            CollectionId = collectionId,
            Image = {'Bytes': image_binary},
            MaxFaces = maxFaces
        )
    
def detectTotalFaces(image_binary):
    response = rekognition.detect_faces(Image = {'Bytes': image_binary}, Attributes=['DEFAULT'])
    return len(response['FaceDetails'])

def printSummary(timestamp, searchFaceConfidenceLevel, totalDetectedFaces, totalMatches):
    print("=============================================================")
    print("Timestamp: " + timestamp)
    print("Total search face confidence level: " + str(searchFaceConfidenceLevel))
    print("Total detected faces: " + str(totalDetectedFaces))
    print("Total matches: " + str(totalMatches))
    print("-------------------------------------------------------------")

def printMatches(matches):
    for index, match in enumerate(matches, start = 1):
        # find person by faceId in dynamodb
        face = dynamodb.get_item(
            TableName = DYNAMO_TABLE_NAME,  
            Key={'FaceId': {'S': match['Face']['FaceId']}}
        )
        
        if 'Item' in face:
            print ("Face " + str(index) + " is recognized as : " + face['Item']['FullName']['S'])
            print ("Matching confidence level: " + str(match['Face']['Confidence']) + "%")

def main():
    while True:
        try:
            # if key down quit taking photo
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # take photo by interval
            attenadanceTime = time.strftime("%Y%m%d-%H%M%S")
            photoPath = ATTENDANCE_RESULT_PATH + attenadanceTime + ".jpg"
            photo = takePhoto(photoPath)
            time.sleep(PHOTO_TAKING_INTERVAL)
            image_binary = convertImageToBytes(photoPath)
            
            # detect and match faces
            response = search_faces_by_image(REKOGNITION_COLLECTION_ID, image_binary, MAX_FACES)
            totalDetectedFaces = detectTotalFaces(image_binary)
            
            # print results
            printSummary(attenadanceTime, response["SearchedFaceConfidence"], totalDetectedFaces, len(response['FaceMatches']))
            printMatches(response['FaceMatches'])

            # TODO: finish upload photo to s3 ATTENDANCE_BUCKET
            # upload photo to s3
            # file = open(photoPath, 'rb')
            # object = s3.Object(ATTENDANCE_BUCKET, photoPath) # replace bucket-name to destinated bucket name
            # object.put(Body = file, Metadata = {
            #     "attenadanceTime": attenadanceTime
            # })
            
        except (KeyboardInterrupt):
            cv2.destroyAllWindow("Bye")
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidParameterException':
                printSummary(attenadanceTime, None, 0) 
            elif e.response['Error']['Code'] == 'InternalServiceError':
                print("An error occurred on service side:", e)
    # exit program
    camera.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    # global config
    PHOTO_TAKING_INTERVAL = 3
    MAX_FACES = 10
    ATTENDANCE_RESULT_PATH = './attendanceSnapshots/'

    # aws configuration
    ANALYST_BUCKET = "analyst-photos"
    ATTENDANCE_BUCKET = "attendance-records"
    DYNAMO_TABLE_NAME = "analystFaces"
    REKOGNITION_COLLECTION_ID = "analystFaces_collection"
    REGION = "ap-southeast-1"

    # initialization
    camera = cv2.VideoCapture(0)
    stream = io.BytesIO()
    s3 = boto3.resource('s3')
    rekognition = boto3.client("rekognition", REGION)
    dynamodb = boto3.client("dynamodb", REGION)
    
    # program starts
    main()