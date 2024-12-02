import cv2
from cvzone.PoseModule import PoseDetector
import math
import numpy as np

# open cv2 capture and pose detector (google mediapipe)
cap = cv2.VideoCapture(0)
detector = PoseDetector(detectionCon=0.7, trackCon=0.7)

class AngleCalc:
    def __init__(self, landmarks, p1, p2, p3, p4, p5, p6, drawPoints):
        self.landmarks = landmarks
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.drawPoints = drawPoints
        self.blue = (255,0,0)
        self.black = (0,0,0)

    def draw_point(self, x, y):
        cv2.circle(img, (x, y), 10, self.blue, 5)
        cv2.circle(img, (x, y), 15, self.black, 6)

    def angle(self):
        if len(self.landmarks) != 0:
            R_Hip = self.landmarks[self.p1]
            R_Knee = self.landmarks[self.p2]
            R_Ankle = self.landmarks[self.p3]
            L_Hip = self.landmarks[self.p4]
            L_Knee = self.landmarks[self.p5]
            L_Ankle = self.landmarks[self.p6]

            # check that there are a valid number of coord points for each joint 
            if len(R_Hip) >= 2 and len(R_Knee) >= 2 and len(R_Ankle) >= 2 and len(L_Hip) >= 2 and len(L_Knee) >= 2 and len(L_Ankle) >= 2:
                x1, y1 = R_Hip[:2]
                x2, y2 = R_Knee[:2]
                x3, y3 = R_Ankle[:2]
                x4, y4 = L_Hip[:2]
                x5, y5 = L_Knee[:2]
                x6, y6 = L_Ankle[:2]

                # calculate angle at the knees using our three points for each leg
                leftKneeAngle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
                rightKneeAngle = math.degrees(math.atan2(y6 - y5, x6 - x5) - math.atan2(y4 - y5, x4 - x5))

                leftKneeAngle = int(np.interp(leftKneeAngle, [30, 180], [100, 0]))
                rightKneeAngle = int(np.interp(rightKneeAngle, [30, 180], [100, 0]))

                # drawing circles and lines on selected points
                if self.drawPoints:
                    self.draw_point(x1, y1)
                    self.draw_point(x2, y2) 
                    self.draw_point(x3, y3)
                    self.draw_point(x4, y4)
                    self.draw_point(x5, y5)
                    self.draw_point(x6, y6)
                    print(x1, y1)

                    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
                    cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 4)
                    cv2.line(img, (x4, y4), (x5, y5), (0, 0, 255), 4)
                    cv2.line(img, (x5, y5), (x6, y6), (0, 0, 255), 4)
                    cv2.line(img, (x1, y1), (x4, y4), (0, 0, 255), 4)

                # total right side visibility score
                right_visibility = (           
                    self.landmarks[self.p1][2] +  
                    self.landmarks[self.p2][2] +  
                    self.landmarks[self.p3][2]   
                )

                # total left side visibility score
                left_visibility = (
                    self.landmarks[self.p4][2] +  
                    self.landmarks[self.p5][2] +  
                    self.landmarks[self.p6][2]   
                )

                if right_visibility > left_visibility:
                    return rightKneeAngle
                else:
                    return leftKneeAngle
                
                # return [leftKneeAngle, rightKneeAngle]

# variables
counter = 0
direction = 0
blue = (255,0,0)
black = (0,0,0)

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))

    detector.findPose(img, draw=0)
    Landmarks, bboxInfo = detector.findPosition(img, bboxWithHands=0, draw=False)

    # point numbers taken from google mediapipe documentation
    angles = AngleCalc(Landmarks, 24, 26, 28, 23, 25, 27, drawPoints=True)
    legs = angles.angle()
    # left, right = legs[0:]

    if legs <= 95:
        if direction == 0:
            counter += 0.5
            direction = 1

    if legs >= 100:
        if direction == 1:
            counter += 0.5
            direction = 0


    # if left <= 95 and right <= 95:
    #     if direction == 0:
    #         counter += 0.5
    #         direction = 1
# 
    # if left >= 85 and right >= 85:
    #     if direction == 1:
    #         counter += 0.5
    #         direction = 0


    # putting scores on the screen
    cv2.putText(img, str(int(counter)), (1200, 80), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 0), 6)

    ## Converting values for rectangles
    progress = np.interp(legs, [0, 100], [650, 450])

    value_right = np.interp(legs, [0, 100], [0, 100])

    # Drawing the empty bar (the outline)
    cv2.rectangle(img, (1125, 450), (1175, 650), black, 5)  # Green border for the bar

    # Drawing the filled bar based on squat progress
    cv2.rectangle(img, (1125, int(progress)), (1175, 650), blue, -1)  # Blue fill for the bar

    # Adding a label for the bar
    cv2.putText(img, 'Squat Bar', (1050, 430), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)

    ## Adding a percentage display for progress
    #percentage = int(np.interp(right, [0, 100], [0, 100]))
    #cv2.putText(img, f'{percentage}%', (1120, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)


    cv2.imshow("image", img)
    cv2.waitKey(1)