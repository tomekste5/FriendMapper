from numpy import index_exp
import requests
import json

from datetime import datetime

steamId = "76561198419672323"
layerDepth = 0
friendsLayerOne = []
overlapCount = []
friendsSince = []
key  = "_::*Ä*:_*"
threshold = 2
autoThreshold = 1
treshAvg = 0


def parseFriends():
    payload = "https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key=" + key+ "&steamid="+steamId
    response =  requests.get(payload)

    parsedFriends = response.json()
    pyObj = json.loads(json.dumps(parsedFriends))
    par = pyObj["friendslist"]["friends"]
    for friend in par:
        friendsLayerOne.append(friend["steamid"])
        overlapCount.append(0)
        friendsSince.append(friend["friend_since"])

def getIdPos(id):
    idx = 0
    for fId in friendsLayerOne:
        if fId == id:
            return idx
        idx += 1
    return -1

def sort():
    for ptr in range(0,len(overlapCount)):
        for i in range(0,len(overlapCount)):
            if(overlapCount[i] < overlapCount[ptr]):
                temp = friendsLayerOne[i]
                friendsLayerOne[i] = friendsLayerOne[ptr]
                friendsLayerOne[ptr] = temp

                temp = overlapCount[i]
                overlapCount[i] = overlapCount[ptr]
                overlapCount[ptr] = temp#

def mapFriends(layer, id):
    if(layer <= layerDepth):
        payload = "https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key=" + key+ "&steamid="+id +"&relationship=friend"
        print(payload)
        response =  requests.get(payload)

        if(response.status_code == 200):
            parsedFriends = response.json()
            pyObj = json.loads(json.dumps(parsedFriends))
            par = pyObj["friendslist"]["friends"]

            for friend in par:
                i = getIdPos(friend["steamid"])
                if i >= 0:
                    overlapCount[i] += 1
                    mapFriends(layer+1,friend["steamid"])
def calcAvg():
    temp = 0
    idx = 0
    global treshAvg
    for id in range(len(friendsLayerOne)):
        if overlapCount[id] >= threshold:
           temp += overlapCount[id]
           idx += 1
        else: break
    treshAvg = temp / idx

def mapToFile():
    jsObj = {}
    sort()
    calcAvg()
    for id in range(len(friendsLayerOne)):
        if overlapCount[id] >= threshold:
            jsObj[friendsLayerOne[id]] = overlapCount[id],datetime.fromtimestamp(int(friendsSince[id])).strftime('%d-%m-%Y %H:%M:%S'),(overlapCount[id] -treshAvg)
        else: break
    json_obj = json.dumps(jsObj,indent=4)

    jsonFile = open("data.json", "w")
    jsonFile.write(json_obj)
    jsonFile.close()

def main():
    parseFriends()
    for friend in friendsLayerOne:
        mapFriends(0,friend)
    mapToFile()

if __name__ == "__main__":
    main()    
