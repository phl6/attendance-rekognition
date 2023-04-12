import cv2
import time
import boto3
import io
from PIL import Image

PHOTO_TAKING_INTERVAL = 3
ATTENDANCE_BUCKET = "attendance-records"
ATTENDANCE_RESULT_PATH = './attendanceSnapshots/'
DYNAMO_TABLE_NAME = "analystFaces"
REKOGNITION_COLLECTION_ID = "analystFaces_collection"
LOCATION = "ap-southeast-1"

rekognition = boto3.client("rekognition", "ap-southeast-1")
dynamodb = boto3.client("dynamodb", "ap-southeast-1")

# initialization
stream = io.BytesIO()
camera = cv2.VideoCapture(0)
s3 = boto3.resource('s3')

def takePhoto(photoName):
    # take photo
    result, photo = camera.read()
    # save photo
    cv2.imwrite(photoName, photo)
    return photo

while True:
    try:
        # if key down quit taking photo
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # take photo by interval
        attenadanceTime = time.strftime("%Y%m%d-%H%M%S")
        photoName = ATTENDANCE_RESULT_PATH + attenadanceTime + ".jpg"
        photo = takePhoto(photoName)
        time.sleep(PHOTO_TAKING_INTERVAL)

        # compare faces
        image = Image.open(photoName)
        image.save(stream, format = "JPEG")
        image_binary = stream.getvalue()
        
        response = rekognition.search_faces_by_image(
            CollectionId = REKOGNITION_COLLECTION_ID,
            Image = {'Bytes': image_binary},
            MaxFaces = 10                                  
        )
        # print("response>>>>" + str(response))
        print("-------------------------------------------------------------")
        print("Total search face confidence level: " + str(response["SearchedFaceConfidence"]))
        print("Time: " + attenadanceTime)
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
            # print("-------------------------------------------------------------")

        # upload photo to s3
        # file = open(photoName, 'rb')
        # object = s3.Object(ATTENDANCE_BUCKET, photoName) # replace bucket-name to destinated bucket name
        # object.put(Body = file, Metadata = {
        #     "attenadanceTime": attenadanceTime
        # })
        
    except (KeyboardInterrupt):
        cv2.destroyAllWindow("Bye")

camera.release()
cv2.destroyAllWindows()