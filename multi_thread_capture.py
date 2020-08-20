import datetime
import threading
import time

import cv2
from threading import Thread

import keyboard

frame_ctr = 0
img_ctr = 0
def capture_cam0(lock, e):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        exit(0)

    #video_images = 'C:\\Users\\hkecl\\PycharmProjects\\cam_calibration\\intrinsics0\\'
    video_images = 'C:\\Users\\hkecl\\OneDrive\\Documents\\Summer2020Research\\openpose\\examples\\media\\'
    # iterate all frames
    global frame_ctr
    global img_ctr
    a = datetime.datetime(2020, 7, 23, 12, 50, 0, 0)
    while (datetime.datetime.now() < a):
        print(".")
    while True:
        #time.sleep(2)
        ret, frame = cap.read()
        t=time.time()
        if ret is False:
            break
        if frame_ctr % 2 == 0 and e.isSet():
            #print("time: {}, ct: {}",t, frame_ctr)
            image_name = video_images + str(img_ctr) + '.jpg'

            cv2.imwrite(image_name, frame)
            print(image_name)
            with lock:
                frame_ctr += 1



    cap.release()


def capture_cam1(lock, e):
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        exit(0)

    #video_images = 'C:\\Users\\hkecl\\PycharmProjects\\cam_calibration\\intrinsics0\\'
    video_images = 'C:\\Users\\hkecl\\OneDrive\\Documents\\Summer2020Research\\openpose\\examples\\media_1\\'
    # iterate all frames
    total_frame = 0
    global frame_ctr
    global img_ctr
    a = datetime.datetime(2020,7,23, 12,50, 0, 0)
    while(datetime.datetime.now() < a):
        print(".")

    while True:
        ret, frame = cap.read()
        t = time.time()
        if ret is False:
            break

        if frame_ctr % 2 == 1 and e.isSet():
            #print("time: {}, ct: {}",t, frame_ctr)

            image_name = video_images + str(img_ctr) + '_0.jpg'
            img_ctr += 1
            cv2.imwrite(image_name, frame)
            print(image_name)
            with lock:
                e.clear()
                frame_ctr += 1


    cap.release()


if __name__ == '__main__':
    lock = threading.Lock()
    e = threading.Event()
    w = threading.Thread(target=capture_cam0, args=(lock, e))
    nw = threading.Thread(target=capture_cam1, args=(lock, e))

    w.start()
    nw.start()

    while True:
        if keyboard.is_pressed('space'):
            e.set()
