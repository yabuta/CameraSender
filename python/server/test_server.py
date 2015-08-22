#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" 
webcamera server 
for opencv 3.0
"""  

import SocketServer  
import cv2
import numpy  
import socket  
import sys
import datetime
import ConfigParser
import readSetting as RS
import insertRDB as irdb
import AESClass as aes

#for OpenCV3.0 python interface  

picturePath = ''

class TCPHandler(SocketServer.BaseRequestHandler):
    
    def handle(self):

        recvlen=100
        buffer=''
        while recvlen>0:
            data = self.request.recv(1024)
            buffer +=data
            recvlen=len(data)        

        #split timestamp and image
        try:
            tm,image = buffer.split("\t",1)
        except Exception as e:
            print >> sys.stderr,e.message
            return

        print str(tm)
        print '%d bytes received' %len(buffer)
        if len(buffer) == 0:
            print >> sys.stderr, "error:received size is 0.\n"
            return
        elif len(tm) == 0:
            print >> sys.stderr,"timestamp is nothing.\n"
            return
        elif len(image) == 0:
            print >> stderr,"image data is nothing"
            return

        irdb.insertData(image,tm)

        #store to imege file
        narray=numpy.fromstring(image,dtype='uint8')
        decimg=cv2.imdecode(narray,1)
        filename = 'result.jpg'
        cv2.imwrite(filename,decimg)

        en = aes.AESCipher('password')
        image = en.decrypt(image)
        narray=numpy.fromstring(image,dtype='uint8')
        decimg=cv2.imdecode(narray,1)
        filename = 'decrypt.jpg'
        cv2.imwrite(filename,decimg)




if __name__ == "__main__":  

    #read setting file
    HOST, PORT,picturePath = RS.getSettings()
    if HOST == None:
        print "client is abnormal terminate.\n"
        exit()

    print 'starting server : port %d'%PORT
    server = SocketServer.TCPServer((HOST, PORT), TCPHandler)  
            
    # Activate the server; this will keep running until you  
    # interrupt the program with Ctrl-C    
    server.serve_forever()  
