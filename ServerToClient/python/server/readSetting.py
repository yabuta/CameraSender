#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser

#settingファイルの読み込み　read setting file
def getHostSettings():
    try:
        initfile = ConfigParser.SafeConfigParser()
        initfile.read("../../../.setting/serverToclient_config.ini")

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
        initfile.read("../../../.setting/serverToclient_config.ini")

        return [initfile.get("settings","cert_path"),initfile.get("settings","key_path")]
    except ValueError as e:
        print e.message
        return [None,None]
    except Exception as e:
        print e.message
        return [None,None]



"""
文字列のリストのリストを受け取ってそれぞれについて対応する設定があれば読み込む
portの場合は範囲の確認を行う


入力：リストのリスト
ex) [[settings,port],[settings,host]]

返り値：
　　正常時：入力リストと同じ大きさのリスト
　　異常時：[None]

"""
def getSettings(list):

    try:
        initfile = ConfigParser.SafeConfigParser()
        initfile.read("../../../.setting/serverToclient_config.ini")

        res = []

        if len(list) == 0:
            return [None]

        for l in list:
            #中のリストの大きさが2出ない場合はエラー
            if len(l) != 2:
                return [None]

            #setting読み込み
            setting = initfile.get(l[0],l[1])

            if l[1] == "port":
                if not setting.isdigit():
                    return [None]
                elif int(setting) < 0 and int(setting) > 65535:
                    return [None]
                setting = int(setting)
            res.append(setting)
        return res

    except ValueError as e:
        print e.message
        return [None]

    except Exception as e:
        print e.message
        return [None]
