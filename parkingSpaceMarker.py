import cv2 as cv
import pickle

try:
    with open("posMarked.pkl", "rb") as f:
        posList = pickle.load(f)

except:
    posList = []

w,h = 109, 49

def eventFunction(events, x, y, flags, params):
    if events == cv.EVENT_LBUTTONDOWN:
        posList.append((x,y))

    if events == cv.EVENT_RBUTTONDOWN:
        for (x1, y1) in posList:
            if x1<x<x1+w and y1<y<y1+h:
                posList.remove((x1, y1))

    with open("posMarked.pkl", "wb") as f:
        pickle.dump(posList, f)

while True:
    img = cv.imread("parkImg.png")
    cv.imshow("Image", img)

    cv.setMouseCallback("Image", eventFunction)

    for (x,y) in posList:
        cv.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)
    cv.imshow("Image", img)


    if cv.waitKey(10) == ord("x"):
        break