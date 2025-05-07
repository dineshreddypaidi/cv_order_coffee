"""
Total Steps

    Step 1: Importing required libraries
    Step 2: Start webcam and set dimensions
    Step 3: Load background image
    Step 4: Load mode images (screens for each mode)
    Step 5: Load icon images (small images for user selections)
    Step 6: Initialize variables for hand gesture control
    Step 7: Start the main loop
    Step 8: Gesture recognition and selection
    Step 9: Visual selection animation
    Step 10: Pause for 1 second after a selection
    Step 11: Show selected icons at the bottom of the screen
    Step 12: Show the final image on screen

"""



# Step 1: Importing required libraries

"""
pip install opencv-python cvzone mediapipe

or

pip install opencv-python
pip install cvzone
pip install mediapipe

"""



"""
os module for working with directories and files
cv2 package for image/video handling
cvzone package for hand tracking

"""

import os  
import cv2  
from cvzone.HandTrackingModule import HandDetector  











# Step 2: Start webcam and set dimensions

"""

0 is usually the default webcam
Setting width of the video frame
Setting height of the video frame

"""


cap = cv2.VideoCapture(0)  
cap.set(3, 640)  
cap.set(4, 480)  


# Step 3: Load background image

"""

Main UI background

"""


imgBackground = cv2.imread("resources/Background.png")  













# Step 4: Load mode images (screens for each mode)

"""

loading list of image file names

"""


folderPathModes = "resources/Modes"
listImgModesPath = os.listdir(folderPathModes) 
 
listImgModes = []

for imgModePath in listImgModesPath:
    fullPath = os.path.join(folderPathModes, imgModePath)
    img = cv2.imread(fullPath)  # Read each image
    listImgModes.append(img)  # Add to list










# Step 5: Load icon images (small images for user selections)

"""

loading list of icon image file names

"""


folderPathIcons = "resources/Icons"
listImgIconsPath = os.listdir(folderPathIcons)

listImgIcons = []

for imgIconsPath in listImgIconsPath:
    fullPath = os.path.join(folderPathIcons, imgIconsPath)
    img = cv2.imread(fullPath)
    listImgIcons.append(img)








# Step 6: Initialize variables for hand gesture control

"""

modeType
-------
modeType to keep track of current screen (0, 1, 2)

0	First screen    (step 1)	First image from listImgModes
1	Second screen   (step 2)	Second image from listImgModes
2	Third screen    (step 3)	Third image from listImgModes




selection
---------
When the user shows 1 finger    → selection = 1
When the user shows 2 fingers   → selection = 2
When the user shows 3 fingers   → selection = 3

No selection initially          → selection = -1 




counter
-------
counter is used to measure how long the user holds a specific hand gesture (like 1 finger, 2 fingers, etc.).





selectionSpeed
--------------

selectionSpeed controls how quickly the green ring fills up when a gesture is being held. Once the ring completes a full circle (360 degrees), the gesture is accepted as a selection.
Try with 3, 7,15

"""



modeType = 0 
selection = -1  
counter = 0 
selectionSpeed = 7  







# Detect only 1 hand

detector = HandDetector(detectionCon = 0.8, maxHands = 1)  







# Circle positions for visual feedback

modePositions = [(1136, 196), (1000, 384), (1136, 581)]  









# Pauses for a short time after a selection

counterPause = 0  





# Stores chosen icons for each mode

selectionList = [-1, -1, -1]  







# Step 7: Start the main loop

while True:
    # Read frame from webcam
    success, img = cap.read()  


    # Detect hand in the webcam frame
    # Returns hand info and image with drawings
    hands, img = detector.findHands(img)  




    # Overlay webcam image on the background
    # Place webcam feed inside background
    imgBackground[139:139 + 480, 50:50 + 640] = img  
    
    
    
    
    
    # Show current mode image on right
    imgBackground[0:720, 847:1280] = listImgModes[modeType]  






    # Step 8: Gesture recognition and selection
    
    if hands and counterPause == 0 and modeType < 3:
        # Get the first detected hand
        hand1 = hands[0]  
        
        # List of 5 values (1 if finger up, 0 if down)
        fingers1 = detector.fingersUp(hand1)  
        print(fingers1)





        # Check which gesture is shown and set selection
        
        if fingers1 == [0, 1, 0, 0, 0]:  # Index finger only
            if selection != 1:
                counter = 1  # Reset counter if new selection
            selection = 1
            
        elif fingers1 == [0, 1, 1, 0, 0]:  # Index + middle fingers
            if selection != 2:
                counter = 1
            selection = 2
            
        elif fingers1 == [0, 1, 1, 1, 0]:  # Index + middle + ring
            if selection != 3:
                counter = 1
            selection = 3
            
        else:
            selection = -1  # No valid gesture
            counter = 0
            
            
            
            
            

        # Step 9: Visual selection animation
        
        if counter > 0:
            counter += 1
            
            # Draw animated ellipse showing progress
            cv2.ellipse(
                imgBackground, 
                modePositions[selection - 1], 
                (103, 103),
                0, 
                0, 
                counter * selectionSpeed, 
                (0, 255, 0), 
                20
            )
            
            # If ellipse is full (360 degrees), confirm selection
            
            if counter * selectionSpeed > 360:
                selectionList[modeType] = selection     # Store selection
                modeType += 1                           # Move to next mode
                counter = 0                             # Reset counter
                selection = -1                          # Reset selection
                counterPause = 1                        # Start pause




    # Step 10: Pause for 1 second after a selection
    
    if counterPause > 0:
        counterPause += 1
        if counterPause > 60:  # Roughly 1 second (since waitKey(1) is used)
            counterPause = 0








    # Step 11: Show selected icons at the bottom of the screen
    
    if selectionList[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]  # First icon
    if selectionList[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionList[1]]  # Second icon
    if selectionList[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[2]]  # Third icon

    # Step 12: Show the final image on screen
    
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)  # Refresh every millisecond
