import cv2
import numpy as np
# import imutils
import easyocr

# img = cv2.imread("img1.jpeg")

plateCascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
minArea = 500

reader = easyocr.Reader(['en'])


cap = cv2.VideoCapture(0)
count = 0

while True:
    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    numberPlates = plateCascade .detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img,"NumberPlate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            imgRoi = img[y:y+h,x:x+w]
            # cv2.imshow("ROI",imgRoi)

    cv2.imshow("Result", img)

    try:
        gray = cv2.cvtColor(imgRoi,cv2.COLOR_BGR2GRAY)
        result = reader.readtext(gray)
        print(result)
    except:
        pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()