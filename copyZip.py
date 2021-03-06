#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2018/10/25
#Author: dylan
#Desc: 拷贝压缩到指定目录

import os 
import sys
import shutil

def process(srcTargetPath, dstDir, zipFileName = None):
    dstDir = os.path.abspath(dstDir)
    srctFolderName = os.path.split(srcTargetPath)[1]
    if zipFileName != None:
        dstZipFilePath = os.path.join(dstDir, zipFileName + '.zip')
    else:
        dstZipFilePath =  os.path.join(dstDir, srctFolderName + '.zip')
    cwd = os.getcwd()
    os.chdir(os.path.join(srcTargetPath , '../' ))
    cmd = "{0} a {1} {2}"
    cmd = cmd.format("WinRAR", dstZipFilePath , srctFolderName)
    os.system("echo " + 'excute:' + cmd)
    #执行压缩命令
    os.system(cmd)
    os.chdir(cwd) 