import boto3
import json
import io
from PIL import Image

# ref: https://docs.aws.amazon.com/rekognition/latest/dg/faces-detect-images.html
def detect_faces(photo, bucket, region):
    
    session = boto3.Session(profile_name='default', region_name=region)
    client = session.client('rekognition', region_name=region)

    response = client.detect_faces(Image = {'Bytes': photo}, Attributes=['ALL'])

    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')

        print('Here are the other attributes:')
        print(json.dumps(faceDetail, indent=4, sort_keys=True))

        # Access predictions for individual face details and print them
        print("Gender: " + str(faceDetail['Gender']))
        print("Smile: " + str(faceDetail['Smile']))
        print("Eyeglasses: " + str(faceDetail['Eyeglasses']))
        print("Emotions: " + str(faceDetail['Emotions'][0]))

    return len(response['FaceDetails'])
    
def main():
    BUCKET ='analyst-photos'
    REGION = "ap-southeast-1"
    
    image = Image.open("./resources/3Faces.jpg")
    stream = io.BytesIO()
    image.save(stream, format = "JPEG")
    image_binary = stream.getvalue()

    face_count=detect_faces(image_binary, BUCKET, REGION)
    print("Total Faces detected: " + str(face_count))

if __name__ == "__main__":
    main()
