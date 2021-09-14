import os

extensions = ['mp3', 'wav', 'm4a']


def loadMusicDir(path):
    files = []
    for f in os.listdir(path):
        if f.split('.')[-1] in extensions:
            files.append(os.path.join(path, f))
    return files


def readMusic(path):
    pass


def getMetadata(musicPath):
    artist = ''
    name = ''
    return artist, name
