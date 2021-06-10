import requests

from user_agent import generate_user_agent, generate_navigator, generate_navigator_js
from pprint import pprint


def getUrl(txtArray, jaaj=''):
    URLpart1 = "https://www.google.com/async/torspo?ei="
    URLpart2 = ""
    URLpart3 = ""
    URLpart4 = ""
    URLend = ",_fmt:jspb"
    killMeThisUrlIsFkingShitIWillBeCrazyAtTheEndOfTheDay = ""
    tag1 = 'function(){window.google={kEI:'
    tag2 = 'data-async-context='
    i = 0
    for element in txtArray:
        i += 1
        if tag1 in element:
            URLpart2 = element.split(tag1)[1].split("'")[1]
        if tag2 in element:
            subArray = element.split(tag2)
            for i in range(1, len(subArray)):
                subElement = element.split(tag2)[i].split('"')[1]
                if "emids" in subElement:
                    URLpart3 = subElement.split(':')[-1]
                if "ctx:%" in subElement:
                    URLpart4 = subElement[subElement.find(";"):]
                    killMeThisUrlIsFkingShitIWillBeCrazyAtTheEndOfTheDay = subElement[:subElement.find(";")]

    URLpart4 = URLpart4.replace(';', ',')
    URLpart4 = URLpart4.split(',')
    finalURLpart4 = []
    i = 0

    for e in URLpart4:
        if i == len(URLpart4) - 2:
            finalURLpart4.append('dme:' + jaaj + ',' + killMeThisUrlIsFkingShitIWillBeCrazyAtTheEndOfTheDay)
        finalURLpart4.append(e)
        i += 1
    return URLpart1 + URLpart2 + '&yv=3&async=emids:' + URLpart3 + ',id:lu' + ",".join(finalURLpart4) + URLend


# print(generate_user_agent())

# print(generate_user_agent(os=('mac', 'linux')))

# pprint(generate_navigator())

# pprint(generate_navigator_js())


def getFinalURL(men=True):
    """

    :param men: True for men match, False for women. Default True
    :return:
    """
    header = {'User-Agent': str(generate_navigator())}
    url = "https://www.google.com/search?q=roland+garros"

    r = requests.get(url, headers=header)
    content = r.content
    content = content.decode("UTF-8")
    contentLines = content.splitlines()
    if men:
        return getUrl(contentLines)
    # Women
    return getUrl(contentLines, 'null')


"""
header = {'User-Agent': str(generate_navigator_js())}
url = "https://www.google.com/search?q=roland+garros"

r = requests.get(url, headers=header)
content = r.content
content = content.decode("UTF-8")
contentLines = content.splitlines()
expectedUrl = "https://www.google.com/async/torspo?ei=V0nCYILYJ-WAjLsP5_q3qA8&yv=3&async=emids:%2Fg%2F11rg46b13_,id:lu,ctx:%5B%5B%5B3%2C%22%2Fm%2F012xcl%22%5D%0A%2C%5B2%5D%0A%2C%5B1%5D%0A%5D%0A%2Cnull%2C%5B%5B%22ev2%22%2C%22clb%22%2C%22tlb%22%2C%22tv%22%2C%22gs2%22%2C%22msv%22%5D%0A%5D%0A%2Cnull%2C1%2Cnull%2C0%2C%5Bnull%2C%5B%22%2Fg%2F11ljs58syp%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F07bs0%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F012xcl%22%5D%0A%5D%0A%2C2%2C0%5D%0A,dme:null,ct:FR,hl:en,tz:Europe%2FParis,_fmt:jspb"

if 'data-async-context=' in content:
    print("YES generate_navigator_js() a marché")
    print(getUrl(contentLines, 'null'))
    print(expectedUrl)
    print(getUrl(contentLines, 'null') == expectedUrl)


header = {'User-Agent': str(generate_navigator())}
url = "https://www.google.com/search?q=roland+garros"

r = requests.get(url, headers=header)
content = r.content
content = content.decode("UTF-8")
contentLines = content.splitlines()

if 'data-async-context=' in content:
    print("YES generate_navigator() a marché")
    print(getUrl(contentLines, 'null'))
    print(expectedUrl)
    print(getUrl(contentLines, 'null') == expectedUrl)
"""
