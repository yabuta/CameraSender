#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser

#settingファイルの読み込み　read setting file
def getHostSettings():
    try:
        initfile = ConfigParser.SafeConfigParser()
        initfile.read("../../../.setting/config.ini")

        port = initfile.get("settings","port")
        if not port.isdigit():
            return [None,None]
        elif int(port) >= 0 and int(port) <= 65535:
            return [initfile.get("settings","host"),int(port)]
        else:
            return [None,None]
    except ValueError as e:
        print e.message
        return [None,None]
    except Exception as e:
        print e.message
        return [None,None]

def getKeyPath():
    try:
        initfile = ConfigParser.SafeConfigParser()
        initfile.read("../../../.setting/config.ini")

        return [initfile.get("settings","cert_path"),initfile.get("settings","key_path")]
    except ValueError as e:
        print e.message
        return [None,None]
    except Exception as e:
        print e.message
        return [None,None]

