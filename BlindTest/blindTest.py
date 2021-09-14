import sys
from BlindTest.readMusic import *

if __name__ == '__main__':
    argc = len(sys.argv)
    musicDirs = []
    if argc == 1:
        musicDirs.append(os.path.commonpath('Music'))
        # probablement pas comme ça
    else:
        musicDirs = sys.argv[1:]
    musicFiles = []
    for musicDir in musicDirs:
        musicFiles + loadMusicDir(musicDir)

