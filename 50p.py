#https://www.youtube.com/watch?v=Fchzk1lDt7Q

import cv2
import numpy as np



def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",16,255,empty)
cv2.createTrackbar("Threshold2","Parameters",14,255,empty)
cv2.createTrackbar("Area","Parameters",5000,30000,empty)
cv2.createTrackbar('width','Parameters', 835,1000,empty)
cv2.createTrackbar('height','Parameters', 393,1000,empty)


def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        
        area = cv2.contourArea(cnt)
        #areaMin = cv2.getTrackbarPos("Area", "Parameters")
       # if area > areaMin:
        if area > 60000 and area < 70000:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 4)
            #peri = cv2.arcLength(cnt, True)
            #approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #print(len(approx))
          #  x , y , w, h = cv2.boundingRect(approx)
            #cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)

            cv2.putText(imgContour, "50p",  (835,393), cv2.FONT_HERSHEY_SIMPLEX, 2,
                        (0, 0, 0), 2)
            #cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
             #           (0, 255, 0), 2)



while True:
    img = cv2.imread('coin_picture.png',1)
    imgContour = img.copy()

    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
    
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    getContours(imgDil,imgContour)

    cv2.imshow("Result", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break