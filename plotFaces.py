#!/usr/bin/env python
import cv2
import json

def main(imagePath, dectectionResult):
    image = cv2.imread(imagePath)
    file = open(dectectionResult, "r")
    imageHeight, imageWidth, _ = image.shape
    data = json.load(file)
    
    maleCounter = 0
    femaleCounter = 0
    eyeGlassesCounter = 0
    
    #emotion color
    angry = (255, 0, 0) # red
    angryCounter = 0
    disgusted = (252, 250, 250) # white
    disgustedCounter = 0
    fear = (230, 230, 250) # purple
    fearCounter = 0
    happy = (255, 192, 203) # pink
    happyCounter = 0
    calm = (0, 255, 0) # green
    calmCounter = 0
    sad = (0, 0, 255) # blue
    sadCounter = 0
    confused = (150,75,0) # brown
    confusedCounter = 0
        
    for face in data['FaceDetails']:
        box = face['BoundingBox']
        w = int(box["Width"] * imageWidth)
        h = int(box["Height"] * imageHeight)
        x = int(box["Left"] * imageWidth)
        y = int(box["Top"] * imageHeight)
        
        # count gender
        # if face["Gender"]["Value"] == "Male" :
        #     maleCounter += 1
        #     color = (255, 0, 0)
        # else:
        #     femaleCounter += 1
        #     color = (0, 0, 255)

        # count glasses
        if face["Eyeglasses"]["Value"]:
            eyeGlassesCounter += 1
            color = (255,255,0)
            image = cv2.rectangle(image, (x, y), (x + w, y + h), color, 3)
        
        # # emotion
        # match face["Emotions"][0]["Type"]:
        #     case "ANGRY":
        #         color = angry
        #         angryCounter += 1
        #     case "DISGUSTED":
        #         color = disgusted
        #         disgustedCounter += 1
        #     case "FEAR":
        #         color = fear
        #         fearCounter += 1
        #     case "HAPPY":
        #         color = happy
        #         happyCounter += 1
        #     case "CALM":
        #         color = calm
        #         calmCounter += 1
        #     case "SAD":
        #         color = sad
        #         sadCounter += 1
        #     case "CONFUSED":
        #         color = confused
        #         confusedCounter += 1
                
        # image = cv2.rectangle(image, (x, y), (x + w, y + h), color, 3)
            
    print("Total male attendees: " + str(maleCounter))   
    print("Total female attendees: " + str(femaleCounter))
    print("Total attendees with eye glasses: " + str(eyeGlassesCounter))
    
    print("number of angry: " + str(angryCounter))
    print("number of disgusted: " + str(disgustedCounter))
    print("number of fear: " + str(fearCounter))
    print("number of happy: " + str(happyCounter))
    print("number of calm: " + str(calmCounter))
    print("number of sad: " + str(sadCounter))
    print("number of confused: " + str(confusedCounter))
    
    cv2.imwrite('./output.png', image)


if __name__ == "__main__":
    main(r"./resources/chinaAccessDay.png", "./resources/chinaAccessDayResult.json")