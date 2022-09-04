#!/home/victor/documents/cctv/venv/bin/python3

import os
import cv2
import time
import credentials
from datetime import datetime

class VideoRecorder():
    # def __init__(self, name='temp_video.avi', fourcc='MJPG', sizex=640, sizey=480, fps=15):
    def __init__(self,fourcc='mp4v', sizex=640, sizey=480, fps=10, scale_down_show= 100, scale_down_write=60, camera_address=credentials.camera_url):
        """
        name: name of the file
        fourcc: code in use.
        sizex: horizontal size
        sizey: vertical size
        """
        # here add the camera url in the format: 'rtsp://USER:PASSWORD@IP_ADDRESS:554/h264Preview_01_main'
        # this is the format for reolink 410w
        self.camera_address = camera_address

        # Set the fps. It will be used in combination with time.sleep() function later.
        self.fps = fps

        # This is the codec used for recording. mp4v by default
        self.fourcc = fourcc
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)

        #set the frame size (for watching only)
        self.frameSize = (sizex, sizey)

        # Connects to the camera url and returns 2 things:
        # ret: true if connected, false otherwise.
        # frame: the image captured by the camera
        self.video_cap = cv2.VideoCapture(self.camera_address)

        # Get the native frame dimensions and scale them down if needed
        self.width = self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.width = int((self.width*scale_down_show/100)//16*16)
        self.height = self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.height = int((self.height*scale_down_show/100)//16*16)

        # Set the scaled width and height for the recording (multiples of 16) (default resolution is 2560 x 1440)
        self.width_scale = int((self.width*scale_down_write/100)//16*16)
        self.height_scale = int((self.height*scale_down_write/100)//16*16)

        # tupple with the dimensions, used for showing.
        self.dimensions_show = (self.width, self.height)
        # tupple with the dimensions, used for writing .
        self.dimensions_write = (self.width_scale, self.height_scale)

        print(self.dimensions_show)
        print(self.dimensions_write)



    def record(self, video_lenght=0.25, show=False):
        """
        video_lenght: duration of the clip in minutes. Default to ~15 seconds (or 0.25minutes)
        """

        # initilize opencv video writer with the current timestamp
        file_name = datetime.now().strftime("%d%m%Y_%H%M%S")+'.mp4'
        video_out = cv2.VideoWriter(file_name, self.video_writer, self.fps, self.dimensions_write)

        # start timer
        timer_start = time.time()

        try:
            while True:
                # ret: returns True if there is a connection with the camera. False otherwise.
                # video_frame: returns the frame from the camera (image)
                ret, video_frame = self.video_cap.read()
                if ret:
                    # show image (false by default)
                    if show:
                        self.showWindow('frame', video_frame, 0,0)

                    # resize frame: resize the frame. Less than 100 to compress it and save space. A bit of a
                    # quality tradeoff.
                    resized_frame = self.resizeImage(video_frame, 30)
                    # write the resized frame to the file.
                    video_out.write(resized_frame)

                    # sleep x seconds so that the fps is the one specified.
                    time.sleep(1/self.fps)

                    # Press 'q' to exit showing the frame (if 'show' is set to True)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.video_cap.release()
                        cv2.destroyAllWindows()

                    # if the elapsed time is more or equal to the video_lenght set.
                    # Notice that reinitilizing VideoWriter takes a few seconds.
                    if (time.time() - timer_start)/60 >= video_lenght:
                        #  close the current file used to record.
                        video_out.release()

                        timer_start = time.time()

                        file_name = datetime.now().strftime("%d%m%Y_%H%M%S")+'.mp4'
                        video_out = cv2.VideoWriter(file_name, self.video_writer, self.fps, self.dimensions_write)
                else:
                    print('Recording error. Check connection.')
                    break
        except KeyboardInterrupt:
            print('released video cap')
            self.video_cap.release()
            cv2.destroyAllWindows()


    def resizeImage(self, frame, scale_percent):
        # resize it. Using the dimensions_write
        resized_frame = cv2.resize(frame, self.dimensions_write, interpolation=cv2.INTER_AREA)
        return resized_frame

    def showWindow(self, window_name, imgage, x, y):
        #flag 0 means autosize
        cv2.namedWindow(window_name, flags=0)
        cv2.moveWindow(window_name, x, y)
        # cv2.resizeWindow(window_name, self.frameSize[0], self.frameSize[1])
        cv2.resizeWindow(window_name, self.dimensions_show[0], self.dimensions_show[1])
        cv2.imshow(window_name, imgage)

    def start(self):

        try:
            while True:
                ret, frame = self.video_cap.read()
                # print(f'ret: {ret}\tframe: {frame}"')
                if ret:
                    # print(f'ret: {ret}')
                    self.showWindow('frame', frame, 0,0)
                    # cv2.imshow('frame', frame)
                    time.sleep(1/self.fps)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print('released video cap')
                        self.video_cap.release()
                        cv2.destroyAllWindows()
                else:
                    print('ret is false. Check connection')
                    break
        except KeyboardInterrupt:
            print('released video cap')
            self.video_cap.release()
            cv2.destroyAllWindows()


    def recordAndShow(self, video_lenght=0.25):
        """
        video_lenght: duration of the clip in minutes.
        """

        # initilize opencv video writer with the current timestamp
        file_name = datetime.now().strftime("%d%m%Y_%H%M%S")+'.mp4'
        video_out = cv2.VideoWriter(file_name, self.video_writer, self.fps, self.dimensions_write)

        # start timer
        timer_start = time.time()
        try:
            while True:
                # ret: returns True if there is a connection with the camera. False otherwise.
                # video_frame: returns the frame from the camera (image)
                ret, video_frame = self.video_cap.read()
                if ret:
                    # print(f'width: {video_frame.shape[1]}\nheight: {video_frame.shape[0]}')

                    self.showWindow('frame', video_frame, 0,0)
                    # resized_frame = self.resizeImage(video_frame, 60)
                    # write the frame to the file.
                    # video_out.write(resized_frame)

                    # sleep x seconds so that the fps is the one specified.
                    time.sleep(1/self.fps)
                    # print(frame_count)
                    if (time.time() - timer_start)/60 >= video_lenght:
                        #  close the current file used to record.
                        video_out.release()

                        timer_start = time.time()
                        # frame_count = 0
                        file_name = datetime.now().strftime("%d%m%Y_%H%M%S")+'.mp4'
                        video_out = cv2.VideoWriter(file_name, self.video_writer, self.fps, self.dimensions_write)
                else:
                    print('Recording error. Check connection.')
                    break
        except KeyboardInterrupt:
            video_out.release()
            print('released video out')



if __name__ == '__main__':
    vr = VideoRecorder(sizex=1280, sizey=720, scale_down_show=30)
    vr.start()
