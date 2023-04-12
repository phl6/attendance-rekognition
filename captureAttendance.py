import cv2
import time
import boto3

PHOTO_TAKING_INTERVAL = 3
ATTENDANCE_BUCKET = "attendance-records"
ATTENDANCE_RESULT_PATH = './attendanceSnapshots/'

# initialization
camera = cv2.VideoCapture(0)
s3 = boto3.resource('s3')

def takePhoto():
    # take photo
    result, image = camera.read()
    cv2.imshow("Attendance Taking", image)
    # save photo
    attenadanceTime = time.strftime("%Y%m%d-%H%M%S")
    photoName = ATTENDANCE_RESULT_PATH + attenadanceTime + ".png"
    cv2.imwrite(photoName, image)
    return attenadanceTime, photoName

while True:
    try:
        # if key down quit taking photo
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # take photo by interval
        attenadanceTime, photoName = takePhoto()
        time.sleep(PHOTO_TAKING_INTERVAL)
        
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