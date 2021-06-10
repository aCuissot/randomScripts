import requests

from user_agent import generate_user_agent, generate_navigator, generate_navigator_js
from pprint import pprint

# print(generate_user_agent())
# 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)'

# print(generate_user_agent(os=('mac', 'linux')))
# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:36.0) Gecko/20100101 Firefox/36.0'

# pprint(generate_navigator())

# {'app_code_name': 'Mozilla',
#  'app_name': 'Netscape',
#  'appversion': '5.0',
#  'name': 'firefox',
#  'os': 'linux',
#  'oscpu': 'Linux i686 on x86_64',
#  'platform': 'Linux i686 on x86_64',
#  'user_agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
#  'version': '41.0'}

# pprint(generate_navigator_js())


header = {'User-Agent': str(generate_navigator_js())}
url = "https://www.google.com/search?q=roland+garros"

r = requests.get(url, headers=header)
content = r.content
content = content.decode("UTF-8")
contentLines = content.splitlines()

expectedUrl = "https://www.google.fr/async/torspo?ei=V0nCYILYJ-WAjLsP5_q3qA8&yv=3&async=emids:%2Fg%2F11rg46b13_,id:lu,ctx:%5B%5B%5B3%2C%22%2Fm%2F012xcl%22%5D%0A%2C%5B2%5D%0A%2C%5B1%5D%0A%5D%0A%2Cnull%2C%5B%5B%22ev2%22%2C%22clb%22%2C%22tlb%22%2C%22tv%22%2C%22gs2%22%2C%22msv%22%5D%0A%5D%0A%2Cnull%2C1%2Cnull%2C0%2C%5Bnull%2C%5B%22%2Fg%2F11ljs58syp%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F07bs0%22%5D%0A%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%22%2Fm%2F012xcl%22%5D%0A%5D%0A%2C2%2C0%5D%0A,dme:null,ct:FR,hl:en,tz:Europe%2FParis,_fmt:jspb"

# webview.create_window('Hello world', url)
# webview.start()
# if 'data-async-context=' in content:
#     f = open("/tmp/jaaj.pytest2", "w")
#     f.write(content)
#     f.close()

# The file contain the html page content to test getUrl but it should be replace by current html content
f = open("media/a.txt", "r", encoding="utf-8")
content = f.read()
contentLines = content.splitlines()


def getUrl(txtArray):
    URLpart1 = "https://www.google.com/async/torspo?ei="
    URLpart2 = ""
    URLpart3 = ""
    URLpart4 = ""
    URLend = ",_fmt:jspb"
    tag1 = 'function(){window.google={kEI:'
    tag2 = 'data-async-context='
    i = 0
    potentialRes = ""
    for element in txtArray:
        i += 1
        if tag1 in element:
            URLpart2 = element.split(tag1)[1].split("'")[1]
        if tag2 in element:
            subArray = element.split(tag2)
            for i in range(1, len(subArray)):
                print("=======")
                subElement = element.split(tag2)[i].split('"')[1]
                print(subElement)
                if "emids" in subElement:
                    URLpart3 = subElement.split(':')[-1]
                if "ctx:%" in subElement:
                    URLpart4 = subElement[subElement.find(";"):]
    print(URLpart3)
    print(URLpart4)
    return URLpart1 + URLpart2 + '&yv=3&async=emids:' + URLpart3 + ',id:lu' + URLpart4.replace(';', ',') + URLend


# print(content)
print(getUrl(contentLines))
print(expectedUrl)