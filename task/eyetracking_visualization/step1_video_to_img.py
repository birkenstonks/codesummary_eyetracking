import numpy as np
import cv2
import os
import glob
videolist = glob.glob('*.mkv')
output_path = './test/'

print('b4 loop')
for vid in videolist:
    print("in loop")
    path = output_path + vid.split('.')[0]
    try:
        os.mkdir(path)
    except:
        pass
    vidcap = cv2.VideoCapture(vid)


    success, image = vidcap.read()
    count = 0
    flag = True
    while flag:
        success, image = vidcap.read()
        if success:
            filename = str("%d.jpg" % (count))
            filepath = path + filename
            print(f"Creating file... {filename}")
            cv2.imwrite(filepath, image)
            count += 1
        else:
            flag = False
    os.remove(filepath)
