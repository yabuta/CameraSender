#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" 
webcamera server 
for opencv 3.0

クライアントからデータを受け取る
画像データはAES暗号がかけられている
通信はsslで行う
現状はMySQLに日付と画像を格納
NoSQLを使ってみたいという願望がある

settingファイルからポート番号と


"""  

import SocketServer  
import cv2
import numpy  
import socket  
import sys
import datetime
import ConfigParser
import readSetting as RS
import TCPServer as tcpserver
import TCPServerWithSSL as sslserver


#for OpenCV3.0 python interface  

#picturePath = ''

if __name__ == "__main__":  

    #read setting file
    res = RS.getSettings([["settings","host"],["settings","port"]])
    if res != [None]:
        HOST,PORT = res
    else:
        print "fail to get settings for host,port."
        exit()
    res = RS.getSettings([["settings","cert_path"],["settings","key_path"]])
    if res != [None]:
        cert_path, key_path = res
    else:
        print "fail to get settings for cert_path,key_path."
        exit()

    print 'starting server : port %d'%PORT

    # Activate the server; this will keep running until you  
    # interrupt the program with Ctrl-C    
    """
    server = SocketServer.TCPServer((HOST,PORT),
                           tcpserver.testHandler)
    print "listening", server.socket.getsockname()
    server.serve_forever()
    """
    sslserver.MySSL_ThreadingTCPServer((HOST,PORT),sslserver.testHandler,
                                       cert_path,
                                       key_path).serve_forever()
