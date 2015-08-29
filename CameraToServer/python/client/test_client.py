#!/usr/bin/env python
# -*- coding:utf-8 -*-

#2015/8/1
#一定時間ごとに画像をサーバに送信する
#
  
import sys  
import time
import readSettings as RS
import Capture
  
# for opencv 3.0.0
  
# Receive data from the server and shut down  


if __name__ == '__main__':  

    ct = Capture.CaptureThread()
    ct.start()


    time.sleep(1)
    print "input some character for end."
    s = sys.stdin.read(1)

    #cv2.imshow('Capture',frame)
    #key=cv2.waitKey(100)
    #if(int(key)>0): break

    ct.stop()
        
    print "client is normal terminate.\n"
