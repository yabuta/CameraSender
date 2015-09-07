#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser

#settingファイルの読み込み　read setting file
def getSettings():

    try:
        initfile = ConfigParser.SafeConfigParser()
        initfile.read("../../../.setting/serverToclient_client_config.ini")

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

def getPASS():
    try:
        initfile = ConfigParser.SafeConfigParser()
        initfile.read("../../../.setting/serverToclient_client_config.ini")

        return initfile.get("settings","password")
    except Exception as e:
        print e.message
        return None


def get_ca_path():
    try:
        initfile = ConfigParser.SafeConfigParser()
        initfile.read("../../../.setting/serverToclient_client_config.ini")

        return initfile.get("settings","ca_cert_path")
    except ValueError as e: #いらんかも
        print e.message
        return None

    except Exception as e:
        print e.message
        return None
