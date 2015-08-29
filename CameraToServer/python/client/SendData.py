#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket  
import cv2
import time
import threading
import datetime

"""
send picture per 5 second.
when called stop, thread finish.
picture convert from mat to jpeg

"""
class SendThread(threading.Thread):
    
    def __init__(self,HOST,PORT,encrypt):
        super(SendThread,self).__init__()
        self.e = threading.Event()
        self.HOST,self.PORT,self.encrypt = HOST,PORT,encrypt
        self.frame = None
        self.lock = threading.RLock()

    def run(self):
        time.sleep(1)
        while not self.e.is_set():
            start = time.time()
            self.sendImageToServer()
            elapse_time = time.time() - start
            print elapse_time * 1000 , "(ms)"
            time.sleep(5)

    def sendImageToServer(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
        sock.connect((self.HOST,self.PORT)) 

        self.lock.acquire()
        if self.frame != None:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
            jpegstring = cv2.imencode('.jpeg',self.frame,encode_param)[1].tostring()

            jpegstring = self.encrypt.encrypt(jpegstring)
            tm = datetime.datetime.today()

            senddata = str(tm) + '\t' + jpegstring
 
            #test
            print len(senddata)
            sock.send(senddata)
        self.lock.release()
        sock.close()  

    def stop(self):
        self.e.set()
        self.join()

    def getDate(self):
        d = datetime.datetime.today()
        return '%4d-%2d-%2d %2d:%2d:%2d' % (d.year,d.month,d.day,d.hour,d.minute,d.second)

    def setFrame(self,frame):
        with self.lock:
            self.frame = frame

