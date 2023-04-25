#!/usr/bin/env python
import cv2
import json

def main(imagePath, dectectionResult):
    image = cv2.imread(imagePath)
    file = open(dectectionResult, "r")
    imageHeight, imageWidth, _ = image.shape
    data = json.load(file)
        
    for face in data['FaceDetails']:
        box = face['BoundingBox']
        w = int(box["Width"] * imageWidth)
        h = int(box["Height"] * imageHeight)
        x = int(box["Left"] * imageWidth)
        y = int(box["Top"] * imageHeight)
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)
        
    cv2.imwrite('./output.png', image)


if __name__ == "__main__":
    main(r"./resources/chinaAccessDay.png", "./resources/chinaAccessDayResult.json")