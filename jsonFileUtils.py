#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2018/1/28
#Author: dylan
#Desc: json文件工具

import json
from io import open
def _getDataFromFile(filePath):
	with open(filePath , 'r' , encoding = 'UTF-8') as f:
		return f.read()

def _saveDataToFile(filePath ,data):
	with open(filePath , 'w', encoding = 'UTF-8') as f:
		f.write(data)

def getJsonDataFromFile(filePath):
	fileStr = _getDataFromFile(filePath)
	fileData = None
	if(fileStr):
		fileData = json.loads(fileStr)
	return fileData
	
def saveJsonDataToFile(filePath , data):
	dataStr = json.dumps(data, sort_keys=True, ensure_ascii = False , indent=4, separators=(',', ': '))
	_saveDataToFile(filePath , dataStr)
