#!/usr/bin/python
# -*- coding: UTF-8 -*- 


import shutil
import jsonFileUtils
import os
import packageNameReplace
from optparse import OptionParser  
import copyZip
import re
import time
import hashlib
import urllib
import urllib2
import sys
import versionControlUtil
import json
reload(sys)
sys.setdefaultencoding('utf8')

clientServerInfoPath = "../../client/client/res/serverInfo.json" 

debugApkBatPath = "publish_debug.bat"
releaseApkBatPath = "publish_release.bat"

def processFolder(folder):
    folder = folder.replace("/", "\\")
    tempDir = os.path.abspath(os.path.join(folder, "../"))
    src = os.path.join(tempDir, "filemd5List.json")
    dst = os.path.join(folder, "res", "filemd5List.json")
    if os.path.exists(dst):
        os.remove(dst)
    os.system("FileCryTo " + folder)
    os.system("MakeMD5List -dst " + tempDir + " -src " + folder)
    shutil.copy(src, dst)
    os.remove(src)

def copyServerInfo():
    serverInfo = jsonFileUtils.getJsonDataFromFile(clientServerInfoPath)
    serverInfo["frontServerUrl"] = os.environ['FRONT_URL']
    serverInfo["imageUrl"] = os.environ['IMAGE_URL']
    serverInfo["mainServerUrlList"] = []
    serverInfo["mainServerUrlList"].append(os.environ['MAIN_SERVER_URL'])
    jsonFileUtils.saveJsonDataToFile(clientServerInfoPath , serverInfo)
    changeMain()
    
def changeMain():
    if os.environ.get("REMOTE_DEBUG_IP") != None:
        mainPath = "../../client/base/src/main.lua"
        with open(mainPath) as f:
            data = f.read()
        data = re.sub(r'(require\("LuaDebugjit"\)\(")[^"]+', r'\g<1>' + os.environ["REMOTE_DEBUG_IP"], data)
        with open(mainPath, 'w') as f:
            f.write(data)

def buildApk():
    copyServerInfo()
    isDebug = os.environ['DEBUG_APK']
    appKey = os.environ['OPENINSTALL_KEY']
    appPackageName = os.environ['PACKAGE_NAME']
    appName = os.environ['APP_NAME']
    appName = appName.decode('gb2312')
    apkBatPath = ''
    if isDebug == 'true':
        apkBatPath = debugApkBatPath
    else:
        apkBatPath = releaseApkBatPath
    os.chdir('../')
    print(os.getcwd())
    packageNameReplace.run(appPackageName , appKey , appName)
    flag =  os.system(apkBatPath)
    if flag != 0 :
        exit(1)

def cryAndZip():
    cwd = os.getcwd()
    zipPath = "../../client/base/res/client.zip"
    if os.path.exists(zipPath):
        os.remove(zipPath)
    os.chdir('..')
    processFolder("../client/client")
    os.system("FileCryTo ../client/base")
    os.chdir("../client")
    os.system("WinRAR a -k -r -m1 base/res/client.zip client")
    os.chdir(cwd)

def buildIos():
    copyServerInfo()
    cryAndZip()
    #把base文件夹拷过去
    copyFileToMac()

def buildHotHall():
    copyServerInfo()
    os.chdir('..')
    processFolder("../client/client")
    copyZip.process('../client/client' , '../', "HotUpdate")
    setBackendVersion(None)

def buildHotGame(gameName, gameID):
    os.chdir('..')
    path = "../client/game/" + gameName
    processFolder(path)
    #生成blackjack.zip
    copyZip.process(path, path + '/../')
    dstZipFilePath = os.path.abspath("../HotUpdate.zip")
    #把2个包打成HotUpdate.zip
    os.chdir('../client')
    os.system("WinRAR a " + dstZipFilePath + " game/" + gameName)
    os.system("WinRAR a " + dstZipFilePath + " game/" + gameName + ".zip")
    setBackendVersion(gameID)

def setBackendVersion(gameID):
    formatdate = time.strftime("%Y%m%d%H%M%S", time.localtime())
    if gameID == None:
        data = {'action': 'HallHotFix', 'time': formatdate, "type": 2, "version": versionControlUtil.getAutoVersion()}
    else:
        data = {'action': 'GameHotFix', 'time': formatdate, "gameId": gameID, "version": versionControlUtil.getAutoVersion()}
    dataEncode = urllib.urlencode(data)

    sign = hashlib.md5("?" + dataEncode + "&szwhkj56dt90gfpjskdw3p4qm")
    sign = sign.hexdigest()
    dataEncode = dataEncode + "&sign=" + sign

    httpUrl = os.environ['FRONT_URL']
    if os.environ['FRONT_URL'].find("http") == -1:
        httpUrl = "http://" + httpUrl
    reqUrl = httpUrl + '/WS/NewMoblieInterface.ashx?' + dataEncode
    res_data = urllib2.urlopen(reqUrl)
    res = res_data.read()
    res = json.loads(res)
    databuffer = res["data"]
    if databuffer and databuffer["valid"] == True:
        print("setBackendVersion success")
    else:
        raise Exception('setBackendVersion error')

def copyFileToMac():
    path = '~/tmpProjs/' + os.environ['APK_ENVIRON'] + '/' + os.environ['TINGZHU_ID'] + '/frameworks/runtime-src/proj.ios_mac'
    src = os.path.abspath("../../client/base")
    src = src.replace("\\", "/")
    src = src.replace(":/", "/")
    src = "/cygdrive/" + src
    path = path.replace("\\", "/")
    os.system("rsync -e 'ssh -p 1022 -o PubkeyAuthentication=yes -o stricthostkeychecking=no' -r -t --delete " + src + " leying@macbook.dev.wgame200.com:" + path)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-t' , '--buildType' , dest = "buildType")
    (option , args) = parser.parse_args()    
    buildType = option.buildType

    versionControlUtil.getAutoVersion()
    if buildType == 'apk':
        buildApk()
    elif buildType == 'ios':
        buildIos()
    elif buildType == 'hotHall':
        buildHotHall()
    elif buildType == 'hotGame':
        rawGameName = os.environ['GAME_NAME']
        matchRes = re.search(r'.*_([^_]+)_(\d+)', rawGameName)
        gameName = matchRes.group(1)
        gameID = matchRes.group(2)
        buildHotGame(gameName, gameID)