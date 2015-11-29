#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import threading
import readSettings as RS
import SendDataWithSSL as sds
import SendData as sd
import AESClass as aes

"""
capture camera data.
when called stop(), thread finish


"""
class CaptureThread(threading.Thread):
    
    def __init__(self):
        super(CaptureThread,self).__init__()
        self.e = threading.Event()

    def run(self):

        res = RS.getSettings([["settings","host"],["settings","port"],["settings","password"]])
        if len(res) == 3:
            HOST,PORT,PASS = res
        else:
            print "fail to get settings.\nclient is abnormal terminate.\n"
            return

        encrypt = aes.AESCipher(PASS)

        st = sds.SendThread(HOST,PORT,encrypt)
        st.start()

        #global frame
        cameraid = 0
        capture = cv2.VideoCapture(0)
        
        if capture.isOpened() is False:
            st.stop()
            print "Could not open camera"
            return

        while not self.e.is_set():
            #frameの取得
            ret, frame= capture.read()

            if ret == False:
                print "capture error.\n"
                break

            st.setFrame(frame)

            #test when you want to show picture
            #cv2.imshow('Capture',frame)            
            #key=cv2.waitKey(100)
            #if(int(key)>0): break
        st.stop()

    def stop(self):
        self.e.set()
        self.join()

