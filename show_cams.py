#!/usr/bin/env python

import cv2
import numpy as np
from calibration import StereoCamera, StereoPair
import rectification
import threading

left_cam_id = 1
right_cam_id = 2
width = 640
height = 480

def show_camera(cam_id, width, height):
    """
    Show one camera
    """
    cap = cv2.VideoCapture(cam_id)
    
    while True:
        ret, img = cap.read()
        if ret:
            img = cv2.resize(img, (width, height))
            cv2.imshow('single camera', img)
             
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    

def show_cameras(left, right, width, height):

    """
    Show two cameras in a horizontal aligned window
    """
    
    cap_left = cv2.VideoCapture(left)
    w = cap_left.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap_left.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print (w, h)
    
    cap_right = cv2.VideoCapture(right)
    size = (width, height)
    print ("resized to: ", size)
    while True:
        ret1, img1 = cap_left.read()
        ret2, img2 = cap_right.read()

        # Wait until ret1 and ret2 are true since camera setup needs some time.
        if ret1 and ret2:
            img1 = cv2.resize(img1, size)
            img2 = cv2.resize(img2, size)
            cv2.imshow("stereo cameras", np.hstack((img1, img2)))
             
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_left.release()
    cap_right.release()
    cv2.destroyAllWindows()

def show_rectified_cameras(left, right, width, height, stereoCamera):

    """
    Show two rectified cameras in a horizontal aligned window
    """
    
    cap_left = cv2.VideoCapture(left)
    w = cap_left.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap_left.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print (w, h)
    
    cap_right = cv2.VideoCapture(right)
    size = (width, height)
    print ("resized to: ", size)
    while True:
        ret1, img1 = cap_left.read()
        ret2, img2 = cap_right.read()

        # Wait until ret1 and ret2 are true since camera setup needs some time.
        if ret1 and ret2:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            img1 = cv2.resize(img1, size)
            img2 = cv2.resize(img2, size)
            (img1, img2) = rectification.undistort_rectify(stereoCamera, img1, img2)
            img1 = rectification.draw_horizontal_lines(img1)
            img2 = rectification.draw_horizontal_lines(img2)

            cv2.imshow("rectified stereo cameras", np.hstack((img1, img2)))
             
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_left.release()
    cap_right.release()
    cv2.destroyAllWindows()

def show_all(left, right, width, height, stereoCamera):
    """ Show original distorted camera pair and rectified and undistorted camera pair together """

    cap_left = cv2.VideoCapture(left)
    w = cap_left.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap_left.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print (w, h)
    
    cap_right = cv2.VideoCapture(right)
    size = (width, height)
    print ("resized to: ", size)
    while True:
        ret1, img1 = cap_left.read()
        ret2, img2 = cap_right.read()

        # Wait until ret1 and ret2 are true since camera setup needs some time.
        if ret1 and ret2:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            img1 = cv2.resize(img1, size)
            img2 = cv2.resize(img2, size)
            (img1r, img2r) = rectification.undistort_rectify(stereoCamera, img1, img2)
            img1r = rectification.draw_horizontal_lines(img1r)
            img2r = rectification.draw_horizontal_lines(img2r)

            cv2.imshow("stereo cameras", np.hstack((img1, img2)))
            cv2.imshow("rectified stereo cameras", np.hstack((img1r, img2r)))
             
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_left.release()
    cap_right.release()
    cv2.destroyAllWindows()

def record_stereo_video(left, right, width, height, filename):
    """
    Record a stereo video with two cameras.
    """
    
    cap_left = cv2.VideoCapture(left)
    w = cap_left.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap_left.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(w, h)
    
    cap_right = cv2.VideoCapture(right)
    size = (width, height)
    print("resized to: ", size)
    fps = cap_left.get(cv2.CAP_PROP_FPS)
    print("fps: ", fps)
    print("press s to start recording...")

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video1 = cv2.VideoWriter(filename + "L.mp4", fourcc, 15, size)
    video2 = cv2.VideoWriter(filename + "R.mp4", fourcc, 15, size)
    recording = False
    while True:
        ret1, img1 = cap_left.read()
        ret2, img2 = cap_right.read()

        # Wait until ret1 and ret2 are true since camera setup needs some time.
        if ret1 and ret2:
            img1 = cv2.resize(img1, size)
            img2 = cv2.resize(img2, size)
            cv2.imshow("stereo cameras", np.hstack((img1, img2)))

            if recording:
                video1.write(img1)
                video2.write(img2)
             
        if cv2.waitKey(1) & 0xFF == ord('q'): #Stop recording, exit
            break
        elif cv2.waitKey(1) & 0xFF == ord('s'): # Start recording
            recording = True

    print ("videos %sL/R.mp4 save." % filename)
    video1.release()
#    video2.release()
    cap_left.release()
    cap_right.release()
    video2.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
#    show_cameras(left_cam_id, right_cam_id, width, height)
#    t1 = threading.Thread(target=show_camera, args=(1, width, height))
#    t2 = threading.Thread(target=show_camera, args=(2, width, height))
#    t1.start()
#    t2.start()
    show_camera(0, width, height)
    

#    stereoCamera = StereoCamera('calib_params2.yml')
#    show_all(left_cam_id, right_cam_id, width, height, stereoCamera)
#    record_stereo_video(left_cam_id, right_cam_id, width, height, 'stereo')
#    show_camera('stereo.avi', width * 2 , height)
