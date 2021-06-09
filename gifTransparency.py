from PIL import Image
import glob  # use it if you want to read all of the certain file type in the directory
import os

def iter_frames(im):
    try:
        i = 0
        while 1:
            im.seek(i)
            imframe = im.copy()
            if i == 0:
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass

"""
# If we want to  chose only some images
imgs = []
for i in range(596, 691):
    imgs.append("snap" + str(i) + '.png')
    print("scanned the image identified with", i)
"""

if not os.path.isdir("tmp"):
    os.mkdir("tmp")

if len(os.listdir("tmp")) == 0:
    print("Directory is empty")
else:

    im = Image.open('tmp/tenor.gif')
    for i, frame in enumerate(iter_frames(im)):
        frame.save('tmp/test%d.png' % i, **frame.info)

    imgs = glob.glob("tmp/*.png")  # do this if you want to read all files ending with .png

    frames = []
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    frames[0].save('tmp/fire3_PIL.gif', format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=60, loop=0)