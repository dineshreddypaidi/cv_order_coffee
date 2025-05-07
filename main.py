import os  
import cv2  
import time
from cvzone.HandTrackingModule import HandDetector  

class OrderCoffee:
    def __init__(self,camera=0,max_hands=1):
        self.img_background = cv2.imread("resources/Background.png")
        self.cap = self._read_camera(camera)
        self.listImgModes = self.__list_icons_modes("resources/Modes")
        self.listImgIcons = self.__list_icons_modes("resources/Icons")
        
        self.hand_detector = self._hand_detector(max_hands)
        
        self.modeType = 0 
        self.selection = -1
        self.counter = 0
        self.selectionSpeed = 7
        
        self.modePositions = [(1136, 196), (1000, 384), (1136, 581)]
        
        self.counterPause = False
        self.selectionList = [-1, -1, -1]
                
        self.line_y = 200
                
    def _read_camera(self,camera):
        cap = cv2.VideoCapture(camera)
        cap.set(3, 640)  
        cap.set(4, 480)
        return cap
    
    def _hand_detector(self, max_hands, confidence = 0.8):
        return  HandDetector(detectionCon = confidence, maxHands = max_hands)
    
    def __list_icons_modes(self,path):        
        img_list = []
        
        for imgPath in os.listdir(path):
            fullPath = os.path.join(path, imgPath)
            img = cv2.imread(fullPath)
            img_list.append(img)
        
        return img_list
    
    def __selection(self,hand):
        fingers = self.hand_detector.fingersUp(hand)
        if fingers == [0, 1, 0, 0, 0]:
            if self.selection != 1:
                self.counter = 1
            self.selection = 1
            
        elif fingers == [0, 1, 1, 0, 0]:
            if self.selection != 2:
                self.counter = 1
            self.selection = 2
            
        elif fingers == [0, 1, 1, 1, 0]:
            if self.selection != 3:
                self.counter = 1
            self.selection = 3
            
        else:
            self.selection = -1
            self.counter = 0
            
    def __draw_ellipse(self):
        if self.counter > 0:
            self.counter += 1
            # Draw animated ellipse showing progress
            cv2.ellipse(
                self.img_background, 
                self.modePositions[self.selection - 1], 
                (103, 103),
                0, 
                0, 
                self.counter * self.selectionSpeed, 
                (0, 255, 0),
                20
            )
     
    def __draw_line(self):
        start_point = (200, 668)
        
        end_point = (self.line_y,668)
                
        if self.selection == 0:
            if self.line_y > 375:
                self.line_y = 375
                
        if self.selection == 1:
            if self.line_y > 580:
                self.line_y = 580
                
        if self.line_y > 580:
            self.line_y = 580
                     
        if self.counter > 0:
            self.line_y += self.selectionSpeed // 2
                 
        if self.selection > 0:
            cv2.line(
                    self.img_background,
                    start_point,
                    end_point,
                    (145, 245, 22),  # Green
                    11
            )      
            
    def __storemode_and_reset(self):
        if self.counter * self.selectionSpeed > 360:
            self.selectionList[self.modeType] = self.selection     # Store selection
            self.modeType += 1                                     # Move to next mode
            self.counter = 0                             # Reset counter
            self.selection = -1                          # Reset selection
            self.counterPause = True                     # Start pause
              
    def __counter_pause(self):
        if self.counterPause:
            time.sleep(0.7)
            self.counterPause = False
    
    def __set_seleted_options(self):
        if self.selectionList[0] != -1:
            self.img_background[636:636 + 65, 133:133 + 65] = self.listImgIcons[self.selectionList[0] - 1]  # First icon
        if self.selectionList[1] != -1:
            self.img_background[636:636 + 65, 340:340 + 65] = self.listImgIcons[2 + self.selectionList[1]]  # Second icon
        if self.selectionList[2] != -1:
            self.img_background[636:636 + 65, 542:542 + 65] = self.listImgIcons[5 + self.selectionList[2]]  # Third icon
        
    def run(self):
        while True:
            success, img = self.cap.read()
            hands, img = self.hand_detector.findHands(img)
            
            if not success or img is None:
                print("Failed to grab frame")
                break
            
            self.img_background[139:139 + 480, 50:50 + 640] = img
            self.img_background[0:720, 847:1280] = self.listImgModes[self.modeType]
            
            if hands and not self.counterPause and self.modeType < 3:
                self.__selection(hands[0])
                self.__draw_ellipse()
                if self.modeType > 0:
                    self.__draw_line()
                self.__storemode_and_reset()
                
            self.__counter_pause()
            self.__set_seleted_options()
            
            cv2.imshow("Order Coffee", self.img_background)
            if cv2.waitKey(1) == ord('q'):
                break

if __name__ == "__main__":
    app = OrderCoffee()
    app.run()