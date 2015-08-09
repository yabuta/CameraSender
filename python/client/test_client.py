#!/usr/bin/env python
# -*- coding:utf-8 -*-

#2015/8/1
#一定時間ごとに画像をサーバに送信する
#
  
import socket  
import sys  
import numpy  
import cv2
import time
import threading
  
# for opencv 3.0.0
  
HOST, PORT = "localhost", 12345  
  
# Receive data from the server and shut down  
quitflag=False  
recvlen=1  
frame = None
lock = threading.RLock()

"""
send picture per 5 second.
when called stop, thread finish.
picture convert from mat to jpeg

"""
class SendThread(threading.Thread):
    
    def __init__(self):
        super(SendThread,self).__init__()
        self.e = threading.Event()

    def run(self):
        time.sleep(1)
        while not self.e.is_set():
            self.sendImageToServer()
            time.sleep(5)

    def sendImageToServer(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
        sock.connect((HOST,PORT)) 

        lock.acquire()
        if frame != None:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]        
            jpegstring = cv2.imencode('.jpeg',frame,encode_param)[1].tostring()
            print len(jpegstring)
            sock.send(jpegstring)
        lock.release()
        sock.close()  

    def stop(self):
        self.e.set()
        self.join()

"""
capture camera data.
when called stop(), thread finish


"""
class CaptureThread(threading.Thread):
    
    def __init__(self):
        super(CaptureThread,self).__init__()
        self.e = threading.Event()

    def run(self):

        global frame
        cameraid = 0
        capture = cv2.VideoCapture(0)
        
        if capture.isOpened() is False:
            print "Could not open camera"
            return

        while not self.e.is_set():
            #frameの取得
            with lock:
                ret, frame= capture.read()

            if ret == False:
                print "capture error.\n"
                break


            #test when you want to show picture
            #cv2.imshow('Capture',frame)            
            #key=cv2.waitKey(100)
            #if(int(key)>0): break

    def stop(self):
        self.e.set()
        self.join()


if __name__ == '__main__':  

    ct = CaptureThread()
    ct.start()

    st = SendThread()
    st.start()


    time.sleep(1)
    print "input some character for end."
    s = sys.stdin.read(1)

    #cv2.imshow('Capture',frame)
    #key=cv2.waitKey(100)
    #if(int(key)>0): break

    st.stop()
    ct.stop()
        
