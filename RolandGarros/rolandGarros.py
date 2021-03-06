import os
import sys
import time

import requests
import platform
from RolandGarros.getURL import getFinalURL
import webview

"""
assuming that lines will always contain the same data -> C fo

Je sais pas si les données reçu par cet url proviennent de google ou d'un autre organisme
mais je les deteste pour n'avoir pas fait un truc simple!!!
"""


def clearLine(line, haveSpace=False):
    if haveSpace:
        return line.split('"')[1].replace("\xa0", " ")
    return line.split('"')[1]


def clear_console(curr_os):
    if 'pycharm' in os.getcwd().lower() or 'pycharm' in sys.exec_prefix.lower():
        print('\n' * 80)
    elif curr_os == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


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


def getService(fullText):
    tag = '["tsp-sv"]'
    tagPlayer = '["tsp-nd","tsp-db","tsp-el"]'
    splitted = fullText.split(tagPlayer)
    if tag in splitted[1]:
        return ['.', ' ']
    return [' ', '.']


def getStatus(txtArray):
    statusTag1 = '["tsp-lv","tsp-fm"]'
    statusTag2 = '["tsp-sis","tsp-frs","tsp-dnil"]'

    i = 0
    count = 0
    for element in txtArray:
        i += 1
        if statusTag1 in element:
            return clearLine(txtArray[i])
        if statusTag2 in element:
            if '[' in element:
                return clearLine(txtArray[i + 3])
            return clearLine(txtArray[i + 2])


def displayResult(req_url, curr_os, refreshRate=30, simple=True, color=False, displayStats=False):
    """

    :param simple: use the basic display of the score or not.
    :param color: Add color to the stats to show which player is winning, if simple is True, this arg is not pris en compte
    :param req_url: The url of the updated match info file (see RolandGarros.md to find it)
    :param curr_os: current OS to be able to clear and so refresh console
    :param refreshRate: In seconds. Stats should not be updated with a very high frequency, so it is useless refresh it to frequently (on the google page, it is around 15sec)
    :param displayStats: Optional: True if you want to display stats too, False if you dont. Default: False
    """

    # webview.create_window('RG', 'https://www.google.fr/search?q=roland+garros')
    # webview.start()

    isInLive = True
    while (isInLive):
        r = requests.get(req_url, allow_redirects=True)

        content = r.content
        content = content.decode("utf-8")

        contentLines = content.splitlines()

        clear_console(curr_os)

        print(getMatch(contentLines))
        print(getCourt(contentLines))
        if simple:
            print(getPlayers(contentLines))
            print(getService(content))
            print("Score:")
            j1Sets, j2Sets = getSets(contentLines)
            print(j1Sets)
            print(j2Sets)

            print(getJeux(contentLines))
        else:
            print("Score:")
            set1, set2 = getSets(contentLines)
            displayScoreProperly(getPlayers(contentLines), set1, set2, getJeux(contentLines), getService(content), color)

        if displayStats:
            print("===========")
            print("Stats:")
            for stat in getStats(contentLines):
                print(stat)
        status = getStatus(contentLines).lower()
        if not ('direct' in status or 'live' in status):
            isInLive = False
            print("STATUS:" + status)

        time.sleep(refreshRate)


def strPlayerNameCut(str1, str2, maxlen=50):
    if max(len(str1), len(str2)) < maxlen:
        maxlen = max(len(str1), len(str2))
    str1 += " " * (maxlen - len(str1))
    str2 += " " * (maxlen - len(str2))
    str1 += '\t: '
    str2 += '\t: '
    return str1, str2


def strPtsCut(arr1, arr2, arr3, color, maxlen=2):
    str1 = ""
    str2 = ""
    for i in range(len(arr1)):
        if max(len(arr1[i]), len(arr2[i])) < maxlen:
            maxlen = max(len(arr1[i]), len(arr2[i]))
        str1 += " " * (maxlen - len(str1))
        str2 += " " * (maxlen - len(str2))
        if color:
            if int(arr1[i]) > int(arr2[i]):
                str1 += "\033[;32m"  # green
                str2 += "\033[;31m"  # red
            elif int(arr1[i]) < int(arr2[i]):
                str2 += "\033[;32m"  # green
                str1 += "\033[;31m"  # red

        str1 += arr1[i]
        str2 += arr2[i]
        if color:
            str2 += "\033[0m"
            str1 += "\033[0m"
        str1 += " | "
        str2 += " | "
    if arr3:
        if max(len(arr3[0]), len(arr3[1])) < maxlen:
            maxlen = max(len(arr3[0]), len(arr3[1]))
        str1 += " " * (maxlen - len(str1))
        str2 += " " * (maxlen - len(str2))
        str1 += arr3[0]
        str2 += arr3[1]

    return str1, str2


def displayScoreProperly(players, j1Sets, j2Sets, jeux, service, color):

    Line0 = ""
    Line1 = ""
    if color:
        Line1 += "\033[;34m" + service[1] + '\033[0m'
        Line0 += "\033[;34m" + service[0] + '\033[0m'
    else:
        Line1 += service[1]
        Line0 += service[0]
    players0, players1 = strPlayerNameCut(players[0], players[1])
    Line1 += players1
    Line0 += players0
    # si aucun jeu en cours
    if not jeux:
        pts0, pts1 = strPtsCut(j1Sets, j2Sets, None, color)
        Line1 += pts1
        Line0 += pts0
    else:
        pts0, pts1 = strPtsCut(j1Sets, j2Sets, jeux, color)
        Line1 += pts1
        Line0 += pts0
    print(Line0)
    print(Line1)


"""
url = "https://www.google.com/async/torspo?ei=qtXAYIvUMKmSjLsPkP2puAo&yv=3&async=emids:%2Fg%2F11rfwjq3qm,id:lu,ctx:%5B%5B%5B3%2C%22%2Fm%2F012xcl%22%5D%0A%2C%5B2%5D%0A%2C%5B1%5D%0A%5D%0A%2Cnull%2C%5B%5B%22ev2%22%2C%22clb%22%2C%22tlb%22%2C%22tv%22%2C%22gs2%22%2C%22msv%22%5D%0A%5D%0A%2Cnull%2C1%2Cnull%2C0%2C%5Bnull%2C%5B%22%2Fg%2F11ljs58syp%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F07bs0%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F012xcl%22%5D%0A%5D%0A%2C2%2C0%5D%0A,dme:,ct:FR,hl:fr,tz:Europe%2FParis,_fmt:jspb"
url = "https://www.google.com/async/torspo?ei=LQTBYPqdN5mVjLsPg4aSyA4&yv=3&async=emids:%2Fg%2F11nn797dgr,id:lu,ctx:%5B%5B%5B3%2C%22%2Fm%2F012xcl%22%5D%0A%2C%5B2%5D%0A%2C%5B1%5D%0A%5D%0A%2Cnull%2C%5B%5B%22ev2%22%2C%22clb%22%2C%22tlb%22%2C%22tv%22%2C%22gs2%22%2C%22msv%22%5D%0A%5D%0A%2Cnull%2C1%2Cnull%2C0%2C%5Bnull%2C%5B%22%2Fg%2F11ljs58syp%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F07bs0%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F012xcl%22%5D%0A%5D%0A%2C2%2C0%5D%0A,dme:,ct:FR,hl:en,tz:Europe%2FParis,_fmt:jspb"
url = "https://www.google.com/async/torspo?ei=chLCYJfEF--DjLsPwNqU4Ag&yv=3&async=emids:%2Fg%2F11rg2mx8rw,id:lu,ctx:%5B%5B%5B3%2C%22%2Fm%2F012xcl%22%5D%0A%2C%5B2%5D%0A%2C%5B1%5D%0A%5D%0A%2Cnull%2C%5B%5B%22ev2%22%2C%22clb%22%2C%22tlb%22%2C%22tv%22%2C%22gs2%22%2C%22msv%22%5D%0A%5D%0A%2Cnull%2C1%2Cnull%2C0%2C%5Bnull%2C%5B%22%2Fg%2F11ljs58syp%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F07bs0%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F012xcl%22%5D%0A%5D%0A%2C2%2C0%5D%0A,dme:null,ct:FR,hl:fr,tz:Europe%2FParis,_fmt:jspb"
url = "https://www.google.fr/async/torspo?ei=j0XCYMn7OqSOjLsP2dW-0Ac&yv=3&async=emids:%2Fg%2F11rg46b13_,id:lu,ctx:%5B%5B%5B3%2C%22%2Fm%2F012xcl%22%5D%0A%2C%5B2%5D%0A%2C%5B1%5D%0A%5D%0A%2Cnull%2C%5B%5B%22ev2%22%2C%22clb%22%2C%22tlb%22%2C%22tv%22%2C%22gs2%22%2C%22msv%22%5D%0A%5D%0A%2Cnull%2C1%2Cnull%2C0%2C%5Bnull%2C%5B%22%2Fg%2F11ljs58syp%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F07bs0%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F012xcl%22%5D%0A%5D%0A%2C2%2C0%5D%0A,dme:null,ct:FR,hl:en,tz:Europe%2FParis,_fmt:jspb"
url = "https://www.google.com/async/torspo?ei=tU_CYL_UFMOMlwTGu7HYBg&yv=3&async=emids:%2Fg%2F11rg46b13_,id:lu,ctx:%5B%5B%5B3%2C%22%2Fm%2F012xcl%22%5D%0A%2C%5B2%5D%0A%2C%5B1%5D%0A%5D%0A%2Cnull%2C%5B%5B%22ev2%22%2C%22clb%22%2C%22tlb%22%2C%22tv%22%2C%22gs2%22%2C%22msv%22%5D%0A%5D%0A%2Cnull%2C1%2Cnull%2C0%2C%5Bnull%2C%5B%22%2Fg%2F11ljs58syp%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F07bs0%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F012xcl%22%5D%0A%5D%0A%2C2%2C0%5D%0A,dme:null,ct:FR,hl:fr,tz:Europe%2FParis,_fmt:jspb"
"""

currOs = platform.system()
url = getFinalURL(False)

# Because getFinalURL is capricieux, si ça marche, on save l'url pour plus tard
if url:
    f = open("tmp_url_save", "w")
    f.write(url)
    f.close()
else:
    f = open("tmp_url_save", "r")
    url = f.read()
    f.close()

displayResult(url, currOs, refreshRate=15, simple=False, color=True)
