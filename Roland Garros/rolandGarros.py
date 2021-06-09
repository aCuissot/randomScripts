import requests


def clearLine(line, haveSpace=False):
    if haveSpace:
        return line.split('"')[1].replace("\xa0", " ")
    return line.split('"')[1]


url = "https://www.google.com/async/torspo?ei=qtXAYIvUMKmSjLsPkP2puAo&yv=3&async=emids:%2Fg%2F11rfwjq3qm,id:lu,ctx:%5B%5B%5B3%2C%22%2Fm%2F012xcl%22%5D%0A%2C%5B2%5D%0A%2C%5B1%5D%0A%5D%0A%2Cnull%2C%5B%5B%22ev2%22%2C%22clb%22%2C%22tlb%22%2C%22tv%22%2C%22gs2%22%2C%22msv%22%5D%0A%5D%0A%2Cnull%2C1%2Cnull%2C0%2C%5Bnull%2C%5B%22%2Fg%2F11ljs58syp%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F07bs0%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F012xcl%22%5D%0A%5D%0A%2C2%2C0%5D%0A,dme:,ct:FR,hl:fr,tz:Europe%2FParis,_fmt:jspb"
url = "https://www.google.fr/async/torspo?ei=LQTBYPqdN5mVjLsPg4aSyA4&yv=3&async=emids:%2Fg%2F11nn797dgr,id:lu,ctx:%5B%5B%5B3%2C%22%2Fm%2F012xcl%22%5D%0A%2C%5B2%5D%0A%2C%5B1%5D%0A%5D%0A%2Cnull%2C%5B%5B%22ev2%22%2C%22clb%22%2C%22tlb%22%2C%22tv%22%2C%22gs2%22%2C%22msv%22%5D%0A%5D%0A%2Cnull%2C1%2Cnull%2C0%2C%5Bnull%2C%5B%22%2Fg%2F11ljs58syp%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F07bs0%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F012xcl%22%5D%0A%5D%0A%2C2%2C0%5D%0A,dme:,ct:FR,hl:en,tz:Europe%2FParis,_fmt:jspb"

r = requests.get(url, allow_redirects=True)

content = r.content
content = content.decode("utf-8")

contentLines = content.splitlines()

"""
assuming that lines will always contain the same data -> C fo
"""


def getPlayers(txtArray):
    playersTags = '["tsp-nd","tsp-db","tsp-el"]'
    i = 0
    res = []
    for element in txtArray:
        i += 1
        if playersTags in element:
            res.append(clearLine(txtArray[i]))

    return res


def getCourt(txtArray):
    courtTag = '["tsp-lo"]'
    i = 0
    for element in txtArray:
        i += 1
        if courtTag in element:
            return clearLine(txtArray[i])


def getMatch(txtArray):
    courtTag = '["tsp-fm"]'
    i = 0
    for element in txtArray:
        i += 1
        if courtTag in element:
            return clearLine(txtArray[i])


def getSets(txtArray):
    scoreTag1 = '["tsp-flr","tsp-st"]'
    scoreTag2 = '["tsp-nf"]'
    scoreTag3 = '["tsp-lo"]'
    i = 0
    res = []
    for element in txtArray:
        i += 1
        if scoreTag1 in element:
            if scoreTag2 in txtArray[i]:
                if scoreTag3 in txtArray[i + 1]:
                    res.append(clearLine(txtArray[i + 2]))
                else:
                    res.append(clearLine(txtArray[i + 1]))
    res1 = []
    res2 = []
    size = len(res) // 2
    for i in range(size):
        res1.append(res[i])
        res2.append(res[i + size])

    return res1, res2


def getJeux(txtArray):
    jeuTag = '["tsp-g","tsp-fs","tsp-fm"]'
    i = 0
    res = []
    for element in txtArray:
        i += 1
        if jeuTag in element:
            res.append(clearLine(txtArray[i]))
    return res


def getStats(txtArray):
    tagName = '["tsp-lpsr","tsp-cm","tsp-fr","tsp-o64"]'
    tagStat = '["tsp-lpsr","tsp-cm","tsp-lpsc"]'
    tagBreak = '["tsp-lh12"]'
    i = 0
    statName = []
    statValue = []
    for element in txtArray:
        i += 1
        if tagName in element:
            statName.append(clearLine(txtArray[i]))
        if tagStat in element:
            if tagBreak in txtArray[i]:
                statValue.append(clearLine(txtArray[i + 1]) + '/' + clearLine(txtArray[i + 5]))
            else:
                if "\xa0" in txtArray[i]:
                    statValue.append(clearLine(txtArray[i]).replace("\xa0", " "))
                else:
                    statValue.append(clearLine(txtArray[i]))

    res = []
    for i in range(len(statName)):
        res.append([statName[i], statValue[i * 2], statValue[i * 2 + 1]])
    return res


print(getMatch(contentLines))
print(getCourt(contentLines))

print(getPlayers(contentLines))
print("Score:")
j1Sets, j2Sets = getSets(contentLines)
print(j1Sets)
print(j2Sets)

print(getJeux(contentLines))

print("===========")
print("Stats:")
for stat in getStats(contentLines):
    print(stat)
