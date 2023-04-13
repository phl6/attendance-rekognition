import cv2
import time
import boto3
import io
from botocore.exceptions import ClientError

def takePhoto():
    result, photo = camera.read()    
    return photo

def convertImageToBytes(photo):
    is_success, im_buf_arr = cv2.imencode(".jpg", photo)
    return im_buf_arr.tobytes()

def search_faces_by_image(collectionId, image_binary, maxFaces):
    return rekognition.search_faces_by_image(
            CollectionId = collectionId,
            Image = {'Bytes': image_binary},
            MaxFaces = maxFaces
        )
    
def detectTotalFaces(image_binary):
    response = rekognition.detect_faces(
            Image = {'Bytes': image_binary}, 
            Attributes = ['DEFAULT']
        )
    return len(response['FaceDetails'])

def printSummary(timestamp, searchFaceConfidenceLevel, totalDetectedFaces, totalMatches):
    print("=============================================================")
    print("Timestamp: " + timestamp)
    print("Total search face confidence level: " + str(searchFaceConfidenceLevel))
    print("Total detected faces: " + str(totalDetectedFaces))
    print("Total matches: " + str(totalMatches))

def printMatches(matches):
    for index, match in enumerate(matches, start = 1):
        # find person by faceId in dynamodb
        face = dynamodb.get_item(
            TableName = DYNAMO_TABLE_NAME,  
            Key={'FaceId': {'S': match['Face']['FaceId']}}
        )
        
        if 'Item' in face:
            print("-------------------------------------------------------------") 
            print ("Face " + str(index) + " is recognized as : " + face['Item']['FullName']['S'])
            print ("Similarity: " + str(match['Similarity']) + "%")
            print ("Matching confidence level: " + str(match['Face']['Confidence']) + "%")

def main():
    while True:
        try:
            # if key down quit taking photo
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # take photo and convert to bytes
            attenadanceTime = time.strftime("%Y%m%d-%H%M%S")
            photo = takePhoto()
            image_bytes = convertImageToBytes(photo)
            
            # detect and match faces
            response = search_faces_by_image(REKOGNITION_COLLECTION_ID, image_bytes, MAX_FACES)
            totalDetectedFaces = detectTotalFaces(image_bytes)
            
            # print results
            printSummary(attenadanceTime, response["SearchedFaceConfidence"], totalDetectedFaces, len(response['FaceMatches']))
            printMatches(response['FaceMatches'])

            # save photo locally for backup
            photoPath = ATTENDANCE_RESULT_PATH + attenadanceTime + ".jpg"
            cv2.imwrite(photoPath, photo)

            # upload photo to s3
            attendanceBucket = s3.Object(ATTENDANCE_BUCKET, attenadanceTime)
            attendanceBucket.put(Body = image_bytes, Metadata = {
                "attenadanceTime": attenadanceTime
            })
            
            time.sleep(PHOTO_TAKING_INTERVAL)
        except (KeyboardInterrupt):
            cv2.destroyAllWindow("Bye")
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidParameterException':
                printSummary(attenadanceTime, None, totalDetectedFaces, 0) 
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