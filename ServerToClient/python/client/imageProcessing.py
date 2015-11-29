#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cv2
import threading
import numpy
import readSettings as RS
import AESClass as aes

class ImageProcessingThread(threading.Thread):

    def __init__(self):
        super(ImageProcessingThread,self).__init__()
        self.lock = threading.RLock()
        self.e = threading.Event()
        self.image = None

        #read password for AED from setting file
        PASSWORD = RS.getSettings([["settings","password"]])
        if PASSWORD == [None]:
            self.decrypt = None
        else:
            self.decrypt = aes.AESCipher(PASSWORD[0])


    def setImage(self,image):
        with self.lock:
            self.image = image

    def decryptImage(self,image):
        if self.decrypt == None:
            #test
            print "decrypt error."
            return None

        decryptimage = self.decrypt.decrypt(image)
        narray=numpy.fromstring(decryptimage,dtype='uint8')
        decimg=cv2.imdecode(narray,1)
        return decimg

    def stop(self):
        self.e.set()
        self.join()

class ImageShow(ImageProcessingThread):

    def __init__(self):
        super(ImageShow,self).__init__()

    def run(self):
        while not self.e.is_set():
            self.imageShow()

    def imageShow(self):
        with self.lock:
            if self.image != None:
                cv2.imshow('test',self.image)
                cv2.waitKey(100)

    def setImage(self,image):
        self.image = self.decryptImage(image)
