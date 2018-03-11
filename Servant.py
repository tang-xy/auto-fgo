import time
import numpy as np
import os
import cv2
import config



def getcoorbynumber(num):
    if num == 1:
        return config.skill_goal1
    elif num == 2:
        return config.skill_goal2
    elif num == 3:
        return config.skill_goal3
    else:
        raise ValueError 

def getcoorbypic(img, template):
    """get top_left for template in img,if not find, return None
    """
    #img=cv2.imread("pic/b.bmp",2)
    img2 = img.copy()  
    #template = cv2.imread("pic/kongming.bmp",0)  
    #w,h = template.shape[::-1]
  
    # 6 中匹配效果对比算法  
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',  
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']  
    methods = ['cv2.TM_CCOEFF_NORMED']
    for meth in methods:
        
        img = img2.copy()  
  
        method = eval(meth)  
  
        res = cv2.matchTemplate(img,template,method)  
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  
  
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:  
            top_left = min_loc  
        else:  
            top_left = max_loc  
        #bottom_right = (top_left[0] + w, top_left[1] + h)  
        if np.max(res)<0.9:
            return None
        else:
            return top_left

class Skill:
    def __init____(self,skill,coordinate):
        self.picpath = skill['picpath']
        self.bewrite = skill['bewrite']
        self.name = skill["name"]
        self.coordinate = coordinate
        self.needgoal = skill['needgoal']


    def chick(self, goal=0):
        cmd = 'adb shell input tap {x1} {y1}'.format(
            x1 = self.coordinate[0],
            y1 = self.coordinate[1]
        )
        os.system(cmd)
        time.sleep(1)
        if self.needgoal == True:
            return
        goal_coordinate = getcoorbynumber(goal)
        cmd = 'adb shell input tap {x1} {y1}'.format(
            x1 = goal_coordinate[0],
            y1 = goal_coordinate[1]
        )
        os.system(cmd)
        time.sleep(2)
        return

class Servant:
    def __init__(self,servant):
        self.img = cv2.imread(servant['picpath'] , 0)
        self.skillimg = cv2.imread(servant['skill_picpath'], 2)
        self.coordinate = self.__servantcoor()
        self.skill1 = Skill(
            servant['skill1'],[self.coordinate[0] + config.skill_delta1[0],self.coordinate[1] + config.skill_delta1[1]]
        )
        self.skill2 = Skill(
            servant['skill2'],[self.coordinate[0] + config.skill_delta2[0],self.coordinate[1] + config.skill_delta2[1]]
        )
        self.skill3 = Skill(
            servant['skill3'],[self.coordinate[0] + config.skill_delta3[0],self.coordinate[1] + config.skill_delta3[1]]
        )
        

    def useselfskill(self,num,goal = 0):
        eval('self.skill' + num).chick(goal)

    def __servantcoor(self):
        res = getcoorbypic(self.img,self.skillimg)
        if res == None:
            raise EOFError
        else:
            return res
        
if __name__ == '__main__':
    img=cv2.imread("pic/b.bmp",2)
    img2 = img.copy()  
    template = cv2.imread("pic/kongming.bmp",0)  
    w,h = template.shape[::-1]
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',  
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']  
    methods = ['cv2.TM_CCOEFF_NORMED']
    for meth in methods:
        
        time_start=time.time()
        img = img2.copy()  
  
        method = eval(meth)  
  
        res = cv2.matchTemplate(img,template,method)  
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  
  
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:  
            top_left = min_loc  
        else:  
            top_left = max_loc  
        bottom_right = (top_left[0] + w, top_left[1] + h)  
  
        cv2.rectangle(img,top_left, bottom_right, 255, 2)  
  
        print(meth)  
        time_end=time.time()
        print('totally cost',time_end-time_start)
        print(np.max(res))