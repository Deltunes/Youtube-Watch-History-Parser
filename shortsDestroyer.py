watchRead = open("watch-history.txt", encoding="utf-8").read()
watchList = watchRead.split("},{")
#print(watchList)

newFile = open("watch-history-updated.txt", "w", encoding="utf-8")
bannedWords = ["shorts", "Shorts", "SHORTS", "Saturday Night Live", "Drew Talbert", "Pirate Software", "Dropout", "Nirami", "Gianmarco Soresi", "Evaks", "Etymology Nerd", "Legends of Avantris", "Washington Post Universe", "Team Coco", "Crunchyroll", "ZachSpeaksGiant", "UFD Tech", "American High", "Annag", "Make Some Noise", "ImEvakz"]
for i in range(len(watchList)):
    addWord = True
    for word in bannedWords:
        if word in watchList[i]:
            addWord = False
    if addWord == True:
        newFile.write(watchList[i])
        newFile.write("},{")