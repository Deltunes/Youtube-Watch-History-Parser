import json
import urllib.request
from ast import Index
from urllib.error import HTTPError

def stripName(itemToStrip):
    strippedItem = itemToStrip
    strippedItem = strippedItem.replace(":", "")
    strippedItem = strippedItem.replace('"', "")
    strippedItem = strippedItem.replace(",", "")
    strippedItem = strippedItem.replace("name", "")
    strippedItem = strippedItem.replace("titleUrl", "")
    strippedItem = strippedItem.replace("https//www.youtube.com/watch?v\\u003d", "")
    strippedItem = strippedItem.rstrip(" ")
    strippedItem = strippedItem.lstrip(" ")
    return strippedItem

def findName(strToCheck):
    if ('"name": ' not in strToCheck) or ('From Google Ads' in strToCheck):
        return False
    else:
        return True

def findURL(strToCheck):
    if '"titleUrl": ' not in strToCheck:
        return False
    else:
        return True

def makeExtraSpace(strToMeasure, maxLen):
    extraSpace = ""
    for m in range(maxLen - len(str(strToMeasure))):
        extraSpace += " "
    return extraSpace

def infoToString(infoList, sortType):
    strOutput = ""
    print(infoList)
    if sortType == 1:
        vidAmountInd = 0
        vidLenInd = 1
    elif sortType == 2:
        vidAmountInd = 1
        vidLenInd = 0
    else:
        vidAmountInd = None
        vidLenInd = None
    for l in range(len(infoList)):
        strOutput += f"{str(l + 1)}{makeExtraSpace(l + 1, len(str(len(infoList))))}"
        strOutput += " - "
        strOutput += str(f"{makeExtraSpace(infoList[l][0][vidAmountInd], 5)}{infoList[l][0][vidAmountInd]} video(s) watched")
        strOutput += " - "
        timeInSec = infoList[l][0][vidLenInd]
        hours = timeInSec // 3600
        minutes = (timeInSec - (hours * 3600)) // 60
        seconds = (timeInSec - (hours * 3600) - (minutes * 60))
        timeOutput = f"{hours} hours, {minutes} minutes, and {seconds} seconds watched"
        strOutput += str(f"{timeOutput}{makeExtraSpace(timeOutput, 44)}")
        strOutput += " - "
        strOutput += str(infoList[l][1])
        strOutput += " "
        strOutput += "\n"
    return strOutput

def IDtoLenInSec(idStr):
    video_id = idStr
    #video_id = 'wu2djWZzmz0'
    api_key = "AIzaSyD32Kga1HrT_eiR2qc3FcG2lIxJyk6uKs4"
    try:
        searchUrl = "https://www.googleapis.com/youtube/v3/videos?id=" + video_id + "&key=" + api_key + "&part=contentDetails"
        response = urllib.request.urlopen(searchUrl).read()
        data = json.loads(response)
        all_data = data['items']
        contentDetails = all_data[0]['contentDetails']
        duration = contentDetails['duration']
    except HTTPError:
        print("HTTPError has occurred")
        return -1
    except IndexError:
        print(f"IndexError has occurred: {video_id}")
        duration = "PT0H0M0S"
    durationStr = duration[2:]
    totalLength = 0
    HIndex = durationStr.find("H")
    MIndex = durationStr.find("M")
    SIndex = durationStr.find("S")
    try:
        if HIndex != -1:
            totalLength += int(durationStr[0:HIndex]) * 60 * 60
        if MIndex != -1:
            totalLength += int(durationStr[HIndex+1:MIndex]) * 60
        else:
            MIndex = HIndex
        if SIndex != -1:
            totalLength += int(durationStr[MIndex+1:SIndex])
    except ValueError:
        print(f"ValueError has occurred: {duration}, {video_id}")
        totalLength = 0
    return totalLength

def getUserData():
    sortBy = None
    minVideoWatched = None
    minSecWatched = None
    while sortBy is None:
        try:
            sortBy = int(input("Select Sorting Method:\n\t1) Number of Videos Watched\n\t2) Time Watched\n"))
        except:
            pass
    if sortBy == 1:
        while minVideoWatched == None:
            try:
                minVideoWatched = int(input("Minimum # of videos watched: "))
            except:
                pass
        return sortBy, minVideoWatched
    elif sortBy == 2:
        while minSecWatched == None:
            try:
                minSecWatched = int(input("Minimum hours watched: ")) * 3600
            except:
                pass
        return sortBy, minSecWatched

def inputIntoDict(name, inp1, inp2, dicty):
    if name not in dicty:
        dicty[name] = [inp1, inp2]
    else:
        dicty[name][0] += inp1
        dicty[name][1] += inp2

def removeAdsAndPosts(entry):
    if ("https://www.youtube.com/post/" in entry) or ("From Google Ads" in entry):
        return True
    else:
        return False

sortMethod, sortMeasure = getUserData()

filename = "watch-history.txt"
#filename = "test-file.txt"
watchRead = open(filename, encoding="utf-8").read()
watchList = watchRead.split("},{")

topChannelsDict = {}
strippedName = None
stripURL = None
vidLen = None
itemCount = 0
basePerc = 0
for i in watchList:
    removeAdsAndPosts(i)
    watchItems = i.split("\n")
    watchItems.pop(0)
    if removeAdsAndPosts(i):
        continue
    for j in watchItems:
        if findName(j):
            strippedName = stripName(j)
        if findURL(j):
            stripURL = stripName(j)
            vidLen = IDtoLenInSec(stripURL)

    if strippedName is not None:
        if sortMethod == 1:
            inputIntoDict(strippedName, 1, vidLen, topChannelsDict)
        elif sortMethod == 2:
            inputIntoDict(strippedName, vidLen, 1, topChannelsDict)

    currentPerc = int(itemCount/len(watchList)*10000) / 100
    if currentPerc > basePerc:
        print(f"{currentPerc} % complete")
        basePerc = currentPerc
    itemCount += 1
topChSortListUncut = sorted([(value,key) for (key,value) in topChannelsDict.items()])
topChSortListUncut.reverse()
topChSortList = []
for m in topChSortListUncut:
    print(m)
    if m[0][0] >= sortMeasure:
        topChSortList.append(m)
print(topChSortList)
input()

channelOutput = infoToString(topChSortList, sortMethod)
newFile = open("top-channel-ranking.txt", "w", encoding="utf-8")
newFile.write(channelOutput)