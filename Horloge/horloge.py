import os
import cv2 as cv
import datetime
from time import sleep
import signal
import sys

chiffres_path = "chiffres.png"
separateur_path = "separateur.png"
new_chiffres_path = "chiffres_bw.png"
ecartement = 5


def createBlackAndWhiteChiffre():
    img = cv.imread(chiffres_path, cv.IMREAD_GRAYSCALE)
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] > 200:
                img[i][j] = 255
            else:
                img[i][j] = 0
    cv.imwrite(new_chiffres_path, img)


# creating this image once to work on it instead of preprocess the first image allow to divide by two the compute time
if not os.path.exists(new_chiffres_path):
    createBlackAndWhiteChiffre()
img_chiffre = cv.imread(new_chiffres_path, cv.IMREAD_GRAYSCALE)


def getChiffreImage(chiffre):
    img = img_chiffre.copy()
    h, w = len(img), len(img[0])

    c1 = chiffre // 5
    c2 = chiffre % 5

    img = img[int(c1 * h / 2):int((c1 + 1) * h / 2), int(c2 * w / 5):int((c2 + 1) * w / 5)]
    """
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] > 200:
                img[i][j] = 255
            else:
                img[i][j] = 0
                """
    return img


def cropImage(img):
    max_col, min_col, max_row, min_row = 0, len(img[0]), 0, 0
    for i in range(len(img)):
        if 0 in img[i]:
            if min_row == 0:
                min_row = i
            max_row = i
        for j in range(len(img[0])):
            if img[i][j] != 255:
                max_col = max(max_col, j)
                min_col = min(min_col, j)
    min_col = max(0, min_col - ecartement)
    max_col = min(max_col + ecartement, len(img[0] - 1))
    return img[min_row:max_row, min_col:max_col]


def getSeparateur():
    img = cv.imread(separateur_path, cv.IMREAD_GRAYSCALE)
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] > 200:
                img[i][j] = 255
            else:
                img[i][j] = 0
    # cv.imshow("", img)
    # cv.waitKey(0)
    return (img)


def fillDateTo2Digits(n):
    if n < 10:
        return "0" + str(n)
    return str(n)


def getDateStr():
    now = datetime.datetime.now()
    return fillDateTo2Digits(now.hour) + ":" + fillDateTo2Digits(now.minute) + ":" + fillDateTo2Digits(now.second)


def hconcat_resize(img_list, interpolation=cv.INTER_CUBIC):
    # take minimum hights
    h_min = min(img.shape[0] for img in img_list)

    # image resizing
    im_list_resize = [cv.resize(img, (int(img.shape[1] * h_min / img.shape[0]), h_min), interpolation=interpolation) for
                      img in img_list]
    return cv.hconcat(im_list_resize)


def display(img):
    columns, rows = os.get_terminal_size(0)
    img = cv.resize(img, os.get_terminal_size(0))
    line = ""
    for i in img:
        for j in i:
            if j == 0:
                line += "A"
            else:
                line += " "
        print(line)
        line = ""


"""
cv.imshow("",  getChiffreImage(5))
cv.waitKey(0)
cv.imshow("",  cropImage(getChiffreImage(5)))
cv.waitKey(0)

for i in range(10):
    getChiffreImage(i)

print(getDateStr())
getSeparateur()
"""
"""
curr_date = getDateStr()
imgList=[]
for char in curr_date:
    if char == ':':
        imgList.append(getSeparateur())
    else:
        imgList.append(cropImage(getChiffreImage(int(char))))
#cv.imshow("", hconcat_resize(imgList))
#cv.waitKey(0)g
display(hconcat_resize(imgList))
"""


def dateCompare(old, new):
    s = len(old)
    for i in range(s - 1, -1, -1):
        if old[i] != ':' and old[i] == new[i]:
            return i
    return -1


jaaj = True


def sigterm_handler(_signo, _stack_frame):
    global jaaj
    jaaj = False


# if sys.argv[1] == "handle_signal":

signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigterm_handler)
try:
    imgList = []
    oldDate = ' ' * 8
    while jaaj:
        curr_date = getDateStr()
        a = dateCompare(oldDate, curr_date)
        if a == -1:
            imgList = []
            a = 0
        else:
            imgList = imgList[:a]

        for i in range(a, len(curr_date)):
            char = curr_date[i]
            if char in curr_date[:i]:
                imgList.append(imgList[curr_date[:i].find(char)])
            else:
                if char == ':':
                    imgList.append(getSeparateur())
                else:
                    imgList.append(cropImage(getChiffreImage(int(char))))
        oldDate = curr_date
        # cv.imshow("", hconcat_resize(imgList))
        # cv.waitKey(0)g
        display(hconcat_resize(imgList))

finally:
    print()