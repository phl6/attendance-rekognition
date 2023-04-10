import cv2
import time
import boto3
import datetime

# initialize the camera
camera = cv2.VideoCapture(0)
# initialize s3 client
s3 = boto3.resource('s3')

PHOTO_TAKING_INTERVAL = 3
photoSeq = 0

while True:
    try:
        # if key down quit taking photo
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # take photo every 10 sec
        result, image = camera.read()
        cv2.imshow("Attendance Taking", image)
        photoName = "Photo" + str(photoSeq) + ".png"
        cv2.imwrite(photoName, image)
        time.sleep(PHOTO_TAKING_INTERVAL)
        
        # upload photo to s3
        file = open(photoName, 'rb')
        object = s3.Object('bucket-name', 'index/' + photoName) # replace bucket-name to destinated bucket name
        object.put(Body = file, Metadata = {
            "LoginTime": datetime.datetime.now()
        })
        
        # update photo counter
        photoSeq += 1
        
    except (KeyboardInterrupt):
        cv2.destroyAllWindow("Bye")

camera.release()
cv2.destroyAllWindows()