#!/usr/bin/env python
# -*- coding:utf-8 -*-

import mysql.connector
import numpy
import sys
import traceback
import cv2

def insertData(frame,tm):

    try:
        connect = mysql.connector.connect(user='executor',password='dymon',host='localhost',database='CameraSecurity',charset='utf8')
        cursor = connect.cursor()

        #insert image data
        cursor.execute('insert into ImageData(image,tm) values(%s,%s)',(frame,tm))
        connect.commit()

        #test
        #cursor.execute('select image from ImageData order by id desc limit 1')
        #row = cursor.fetchone()
    
        #for i in row:
        #    narray=numpy.fromstring(i,dtype='uint8')
        #    decimg=cv2.imdecode(narray,1)
        #    filename = 'test.jpg'
        #    cv2.imwrite(filename,decimg)

        cursor.close()
        connect.close()

    except mysql.connector.Error as err:
        print err.msg

    except Exception as e:
        print str(type(e))
        print e.message
        print traceback.format_exc(sys.exc_info()[2])
