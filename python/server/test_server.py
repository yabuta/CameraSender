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

#for OpenCV3.0 python interface  

class TCPHandler(SocketServer.BaseRequestHandler):    

    def handle(self):  
        recvlen=100  
        buffer=''   
        while recvlen>0:
            data = self.request.recv(1024)
            buffer +=data
            recvlen=len(data)
  
        print '%d bytes received' %len(buffer)
        if len(buffer) == 0:
            print >> sys.stderr, "error:received size is 0.\n"
            return
        narray=numpy.fromstring(buffer,dtype='uint8')
        decimg=cv2.imdecode(narray,1)
        d = datetime.datetime.today()
        filename = 'picture/result%d-%d-%d_%d:%d:%d.jpg'%(d.year,d.month,d.day,d.hour,d.minute,d.second)
        cv2.imwrite(filename,decimg)

if __name__ == "__main__":  
    HOST, PORT = 'localhost', 12345  
            
    print 'starting server : port %d'%PORT
    server = SocketServer.TCPServer((HOST, PORT), TCPHandler)  
            
    # Activate the server; this will keep running until you  
    # interrupt the program with Ctrl-C    
    server.serve_forever()  
            
            