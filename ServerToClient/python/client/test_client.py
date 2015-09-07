#!/usr/bin/env python
# -*- coding:utf-8 -*-

#2015/8/1
#一定時間ごとに画像をサーバに送信する
#
  
import sys  
import time
import readSettings as RS
import recvDataWithSSL as rd
import imageProcessing as ip 
 
# for opencv 3.0.0
  
# Receive data from the server and shut down  


if __name__ == '__main__':  

    HOST,PORT = RS.getSettings()
    if HOST == None or PORT == None:
        print "client is abnormal terminate.\n"
        exit()

    ishow = ip.ImageShow()
    st = rd.RecvThread(HOST,PORT,ishow)
    ishow.start()
    st.start()


    time.sleep(1)
    print "input some character for end."
    s = sys.stdin.read(1)

    st.stop()
    ishow.stop()
        
    print "client is normal terminate.\n"
