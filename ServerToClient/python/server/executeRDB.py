#!/usr/bin/env python
# -*- coding:utf-8 -*-

import mysql.connector
import numpy
import sys
import traceback
import cv2


class executeRDB:

    def __init__(self):
        try:
            self.connect = mysql.connector.connect(user='executor',password='dymon',host='localhost',database='CameraSecurity',charset='utf8',buffered=True)
            self.cursor = self.connect.cursor()
            self.error_message = "error"
            self.success_message = "success"

        except mysql.connector.Error as err:
            print "in constractor"
            print "in executeRDB.py"
            print err.msg
            
        except Exception as e:
            print "in constractor"
            print "in executeRDB.py"
            print str(type(e))
            print e.message
            print traceback.format_exc(sys.exc_info()[2])        

    def close(self):
        try:
            self.cursor.close()
            self.connect.close()
        except mysql.connector.Error as err:
            print "in close"
            print "in executeRDB.py"
            print err
            
        except Exception as e:
            print "in close"
            print "in executeRDB.py"
            print str(type(e))
            print e.message
            print traceback.format_exc(sys.exc_info()[2])        




    def getData(self):
        try:
            if self.connect == None or self.cursor == None:
                return self.error_message

            sql = "select image from ImageData order by tm desc limit 1;"
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            data = row[0]

        except mysql.connector.Error as err:
            print "in getData"
            print "in executeRDB.py"
            print err.msg
            return self.error_message
            
        except Exception as e:
            print "in getData"
            print "executeRDB.py"
            print str(type(e))
            print e.message
            print traceback.format_exc(sys.exc_info()[2])        
            return self.error_message

        return data

    def insertData(self,frame,tm):
        
        try:
            if self.connection == None or self.cursor == None:
                return self.error_message

            #insert image data
            self.cursor.execute('insert into ImageData(image,tm) values(%s,%s)',(frame,tm))
            self.connect.commit()

            #test
            #cursor.execute('select image from ImageData order by id desc limit 1')
            #row = cursor.fetchone()
    
            #for i in row:
            #    narray=numpy.fromstring(i,dtype='uint8')
            #    decimg=cv2.imdecode(narray,1)
            #    filename = 'test.jpg'
            #    cv2.imwrite(filename,decimg)

        except mysql.connector.Error as err:
            print "executeRDB.py"
            print err.msg
            
        except Exception as e:
            print "executeRDB.py"
            print str(type(e))
            print e.message
            print traceback.format_exc(sys.exc_info()[2])
            
        return self.success_message


    def isError(self,message):
        if message == self.error_message:
            return true
