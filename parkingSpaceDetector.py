import cv2 as cv
import numpy as np
import pickle
import cvzone

capture = cv.VideoCapture("park.mp4")

with open("posMarked.pkl", "rb") as f:
    posList = pickle.load(f)

w,h = 109, 49

def preProcessImage(img):
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (3,3), 1)
    imgThresh = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv.medianBlur(imgThresh, 5)
    
    kernelSize = np.ones((3,3), np.uint8)
    imgDilate = cv.dilate(imgMedian, kernelSize)

    return imgDilate

def parkingSpaceCounter(preProImg, img):

    spaceTotal = len(posList)
    spaceFree = 0
    spaceOccupied = 0

    for (x,y) in posList:
        imgCrop = preProImg[y:y+h, x:x+w]
        # cv.imshow(str(x*y), imgCrop)
        count = cv.countNonZero(imgCrop)

        if count<800:
            color = (0,255,0)
            thickness = 3
            spaceFree += 1
        else:
            color = (0,0,255)
            thickness = 2
            spaceOccupied += 1

        cv.rectangle(img, (x,y), (x+w,y+h), color, thickness)
        cv.putText(img, str(count), (x+4, y+40), cv.FONT_HERSHEY_COMPLEX, 0.5, color, 1)
        
        dispText = f"Available : {spaceFree}        Occupied : {spaceOccupied}      Total : {spaceTotal}"
        cvzone.putTextRect(img, dispText, (20,40),scale=2.54, offset=20 ,colorR=(0,255,0))


while True:

    # Loop the video
    if capture.get(cv.CAP_PROP_POS_FRAMES) == capture.get(cv.CAP_PROP_FRAME_COUNT):
        capture.set(cv.CAP_PROP_POS_FRAMES, 0)

    ret, img = capture.read()

    preProImg = preProcessImage(img)

    parkingSpaceCounter(preProImg, img)

    cv.imshow("Parking Footage", img)

    if cv.waitKey(10) == ord("x"):
        break

capture.release()
cv.destroyAllWindows()