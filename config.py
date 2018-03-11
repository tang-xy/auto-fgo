import json


try:
    dic = json.load(open("config.json"))
except FileNotFoundError:
    print("Cannot Found Configfile")
    exit(-1)
try:
    screen = dic['screen']
    screen_X = screen['size'][0]
    screen_Y = screen['size'][1]
    skill_goal1 = screen['skill_goal1']
    skill_goal2 = screen['skill_goal2']
    skill_goal3 = screen['skill_goal3']
    skill_delta1 = screen['skill_delta1']
    skill_delta2 = screen['skill_delta2']
    skill_delta3 = screen["skill_delta3"]
except KeyError:
    print("Configfile Error")
    exit(-2)

def getinstancepath(instanceName):
    res = dic['instancePath'][instanceName]
    return res

def getapplepath(appleName):
    res = dic['applePath'][appleName]
    return res

def loadqueue():
    res = dic['queue']
    return res

if __name__ == "__main__":
        pass

