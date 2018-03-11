import cv2
import sys
import time
import autofgo
def auto(fgo):

    fgo.inInstance(fgo.COST_40_FOR_QP)        #进入副本，由预定义宏指定，体力不足时吃苹果
    
    fgo.selectFriend(fgo.LUNCH_KONGMING)      #选择助战好友，午餐孔明
    
    wait()                                    #等待进入
    
    fgo.useSkill('kongming',fgo.BY_NAME,3)    #使用英灵技能，通过1，2参数确定要释放技能的英灵
    fgo.useSkill('kongming',fgo.BY_NAME,2)    #3参数确定释放的技能
    fgo.useSkill("saber",fgo.BY_NAME,3)
    wait()
    fgo.noblephantasmTurn("Excalibur")        #宝具回合
    while(fgo.inturn(2) == False):            #若没进入下一面，则平A补刀
        fgo.budao()
    
    fgo.exchange(1,4)                         #masterSkill交换英灵

    fgo.useSkill("kongming",fgo.BY_NAME,1,1)  #4参数为释放目标
    fgo.useSkill("emiya",fgo.BY_NAME,3)
    fgo.noblephantasmTurn("UBW")
    wait()
    while(fgo.inturn(3) == False):            #若没进入下一面，则平A补刀
        fgo.budao()
    
    fgo.useSkill("Francis Drake",fgo.BY_NAME,3)
    fgo.noblephantasmTurn("Golden Wild Hunt")
    while(fgo.inturn(3) == True):            #若没进入下一面，则平A补刀
        fgo.budao()
    
    fgo.outInstance()

    return

def yes_or_no(prompt, true_value='y', false_value='n', default=True):
    default_value = true_value if default else false_value
    prompt = '%s %s/%s [%s]: ' % (prompt, true_value, false_value, default_value)
    i = input(prompt)
    if not i:
        return default
    while True:
        if i == true_value:
            return True
        elif i == false_value:
            return False
        prompt = 'Please input %s or %s: ' % (true_value, false_value)
        i = input(prompt)

if __name__ == "__main__":
    op = yes_or_no('请确保手机打开了 ADB 并连接了电脑，然后打开跳一跳并【开始游戏】后再用本程序，确定开始？')
    if not op:
        print('bye')
        exit(0)
    fgo = autofgo.fgo3t_env()                           #读入英灵配置文件，初始化环境
    for i in range(15):
        print("现在开始第{0}次本".format(i))
        auto(fgo)
    fgo.exit()