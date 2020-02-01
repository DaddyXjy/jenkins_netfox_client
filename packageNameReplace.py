#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import re
from io import open
import shutil
import os
ANDROID_SRC_CONFIG = "../frameworks/runtime-src/proj.android-studio/app/src/org/cocos2d/hongniu"
ANDROID_BASE_CONFIG = "../frameworks/runtime-src/proj.android-studio/app/src"
ANDROID_RES_CONFIG = "../frameworks/runtime-src/proj.android-studio/app/res"

OLD_PACKAGE_NAME = "org.cocos2d.hongniu"
OLD_APP_KEY = "spjm49"
OLD_APP_NAME = "红牛棋牌"
fileList = [
    "../frameworks/runtime-src/proj.android-studio/app/AndroidManifest.xml",
    "../frameworks/runtime-src/proj.android-studio/app/src/org/cocos2d/hongniu/wxapi/WXEntryActivity.java",
    "../frameworks/runtime-src/proj.android-studio/app/src/org/cocos2d/hongniu/wxapi/WXPayEntryActivity.java",
    "../frameworks/runtime-src/proj.android-studio/app/src/org/cocos2dx/lua/AppActivity.java",
    "../frameworks/runtime-src/proj.android-studio/app/src/org/cocos2dx/thirdparty/ThirdParty.java",
    "../frameworks/runtime-src/proj.android-studio/app/build.gradle"
]

def replaceFileKeyword(filePath , oldName ,  newName , encodingFormat = 'utf-8'):
    fileStream = None
    with open(filePath, 'r', encoding = encodingFormat, errors='ignore') as f:
        fileStream = f.read()
        fileStream = fileStream.replace(oldName , newName)
        print "replace packageName:" + filePath
    if fileStream:
        with open(filePath , 'w', encoding = encodingFormat, errors='ignore') as f:
            f.write(fileStream)

def replaceFilesKeyword(oldpackageName ,  newPackageName):
    for filePath in fileList:
        fileStream = None
        replaceFileKeyword(filePath , oldpackageName , newPackageName)

def setAppName(appName):
	nameConfigPath = os.path.join(ANDROID_RES_CONFIG , 'values\\strings.xml')
	replaceFileKeyword(nameConfigPath , OLD_APP_NAME , appName)

def setWxScriptFolder(packageName):
    t = packageName.split('.')
    gap = '/'
    packagePath = gap.join(t)
    dstTree = os.path.join(os.path.join(ANDROID_BASE_CONFIG , packagePath) , 'wxapi')
    srcTree = os.path.join(ANDROID_SRC_CONFIG , 'wxapi')

    if os.path.exists(dstTree):
        shutil.rmtree(dstTree)
    shutil.copytree(srcTree , dstTree)
    shutil.rmtree(srcTree)

def run(packageName , appKey,appName):
    replaceFilesKeyword(OLD_PACKAGE_NAME , packageName)
    replaceFilesKeyword(OLD_APP_KEY , appKey)
    setWxScriptFolder(packageName)
    setAppName(appName)



if __name__ == "__main__":
    replace("foxuc.qp.Gloqj.mnlwg11" , "foxuc.qp.Gloqj.mnlwg")
    setWxScriptFolder('dd.ee.tt')