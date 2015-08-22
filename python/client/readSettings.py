#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser

#settingファイルの読み込み　read setting file
def getSettings():

    try:
        initfile = ConfigParser.SafeConfigParser()
        initfile.read("../../.setting/client_config.ini")

        port = initfile.get("settings","port")
        if not port.isdigit():
            return [None,None]
        elif int(port) >= 0 and int(port) <= 65535:
            return [initfile.get("settings","host"),int(port),initfile.get("settings","password")]
        else:
            return [None,None]
    except ValueError as e:
        print e.message
        return [None,None]

    except Exception as e:
        print e.message
        return [None,None]
