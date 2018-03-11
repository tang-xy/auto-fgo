from Servant import Servant
import config
import time
from Servant import getcoorbypic
import cv2
import os
import numpy as np

def comparebypic(img, template1,template2):
    """if template1 in img retrunn 0;
    if template2 in img return 1;
        else return none
    """
    meth = 'cv2.TM_CCOEFF_NORMED'
        
  
    method = eval(meth)  
  
    res1 = cv2.matchTemplate(img,template1,method)  
    res2 = cv2.matchTemplate(img,template2,method)  
    
    if (np.max(res1)<0.9) and (np.max(res2)<0.9):
        return None
    
    if np.max(res1)>np.max(res2):
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res1)
      
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:  
            top_left = min_loc  
        else:  
            top_left = max_loc

        return 0,top_left
    else:

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res2)
      
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:  
            top_left = min_loc  
        else:  
            top_left = max_loc
        return 1,top_left

class fgo3t_env:
    def __init__(self,typeApple = 0x5000):
        
        self.COST_40_FOR_QP = 0x0001

        self.BY_NAME = 0x0010
        
        self.ANY_FRIEND = 0x0100
        self.LUNCH_KONGMING = 0x0200

        self.GOLD_APPLE = 0x1000
        self.SILVER_APPLE = 0x2000
        self.COPPER_APPLE = 0x3000
        self.COLOUR_APPLE = 0x4000
        self.NO_APPLE = 0x5000

        self.appletype = typeApple
        queue_dic = config.loadqueue()
        self.queue = {}
        for servant in queue_dic.key():
            self.queue[servant] = Servant(queue_dic[servant])

    def __getscreen(self):
        """get now screen ,return a binary pic  
        """
        os.system('adb shell /system/bin/screencap -p /sdcard/screenshot.png')
        os.system('adb pull /sdcard/screenshot.png ./pic/screenshot.png')
        img = cv2.imread('pic/screenshot.png', 0)
        
        ret2,th2=cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return th2
        
    def useSkill(self,str,wayOrder,skillNumber = 0,goal = 0):
        """str :string for order
           wayOrder: can be BY_NAME or other
           skillNumber: 
        """
        if wayOrder == self.BY_NAME:
            try:
                self.queue[str].useselfskill(skillNumber,goal)
            except KeyError:
                print("There is not "+str+' in your queue!')
                exit(-3)
        time.sleep(0.5)

    def eatapple(self,typeApple):
        if typeApple == self.NO_APPLE:
              print("体力清空")
              exit(1)
        applePath = config.getapplepath(typeApple)
        screen = self.__getscreen()
        applePic = cv2.imread(applePath[0], 2)
        applePicNone = cv2.imread(applePath[1], 2)
        a,goal_coordinate = comparebypic(screen,applePic,applePicNone)
        if a == None:
            print("苹果图片错误！")
            exit(-3)
        if a == 1:
            print("苹果耗尽")
            exit(2)
        cmd = 'adb shell input tap {x1} {y1}'.format(
            x1 = goal_coordinate[0],
            y1 = goal_coordinate[1]
        )
        os.system(cmd)
        time.sleep(2)

    def inInstance(self, instanceName):
        """instanceName:can be COST_40_FOR_QP or other
        """
        if instanceName == self.COST_40_FOR_QP:
            path = config.getinstancepath('COST_40_FOR_QP')
            img = self.__getscreen()
            template1 = cv2.imread(path[0], 2)
            
            template2 = cv2.imread(path[1], 2)
            
            a,top_left = comparebypic(img,template1,template2)
            if a == None:
                print("请确认屏幕内是否存在指定副本")
                exit(-4)

            while a == 1:
                cmd = 'adb shell input tap {x1} {y1}'.format(
                    x1 = top_left[0],
                    y1 = top_left[1]
                )
                os.system(cmd)
                time.sleep(1)
                self.eatapple(self.appletype)

                a,top_left = comparebypic(img,template1,template2)
            cmd = 'adb shell input tap {x1} {y1}'.format(
                x1 = top_left[0],
                y1 = top_left[1]
            )
            os.system(cmd)
            time.sleep(1)

                