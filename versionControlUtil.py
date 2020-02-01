#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2019/01/30
#Author: dylan
#Desc: 版本控制工具

import subprocess
import os
import time
timeAutoVersion = None
def getAutoVersion():
	global timeAutoVersion
	if timeAutoVersion == None:
		timeAutoVersion = str(int(time.time()) - 1571971000)
	os.system("echo git auto version:" + timeAutoVersion)
	return timeAutoVersion