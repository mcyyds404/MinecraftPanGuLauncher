
from concurrent.futures import ThreadPoolExecutor
import os,time
import urllib.request
import json
import re
import platform
import threading as thd
pool = ThreadPoolExecutor(max_workers=20)
def mmkdir(path):
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
def download(url,downloadlocation):
    pool.submit(downloada(url,downloadlocation))
    

def downloada(url,downloadlocation):
    if os.path.exists(downloadlocation):
        pass
    else:
        try:
            url=re.sub(r"https://launchermeta.mojang.com|https://launcher.mojang.com","https://download.mcbbs.net",url)
            url=re.sub(r"https://libraries.minecraft.net","https://download.mcbbs.net/maven",url)
            urllib.request.urlretrieve(url,downloadlocation)
        except:
            pass
        
def Parsingid(u):
    version_manifest=urllib.request.urlopen("https://download.mcbbs.net/mc/game/version_manifest.json")
    time.sleep(4)
    version_manifestjson=json.loads(version_manifest.read())
    version_manifestjson=version_manifestjson["versions"]
    for i in range(len(version_manifestjson)):
        o=version_manifestjson[i]
        if o["id"]==u:
            return version_manifestjson[i]
def versionjson(id,url,downloadlocation):
    mmkdir(downloadlocation+"versions/"+id)
    downloada(url,downloadlocation+"versions/"+id+"/"+id+".json")
    versionjson=open(downloadlocation+"versions/"+id+"/"+id+".json","r")
    versionjson=versionjson.read()
    versionjson=json.loads(versionjson)
    downloadminecraftclient(versionjson["downloads"],downloadlocation+"versions/"+id+"/",id)
    downloadminecraftlibraries(versionjson["libraries"],downloadlocation+"/libraries")
    downloadminecraftasset(versionjson["assetIndex"],downloadlocation+"/assets")
    
def downloadminecraft(id,downloadlocation):
    try:
        mmkdir(downloadlocation+".minecraft")
        mmkdir(downloadlocation+".minecraft/"+"versions/")
    except:
        pass
    
    u=Parsingid(id)
    ut=u["url"]
    versionjson(id,ut,downloadlocation+".minecraft/")


def downloadminecraftclient(json,downloadlocation,id):
    json=json['client']
    url=json["url"]
    download(url,downloadlocation+id+".jar")

def downloadminecraftlibraries(json,downloadlocation):
    mmkdir(downloadlocation)
    for i in range(len(json)):
        u=""
        o=json[i]
        z=o
        if "classifiers" in z["downloads"]:
            z=z["downloads"]["classifiers"]
            if platform.system()=='Windows':
                if "natives-windows" in z:
                    z=z["natives-windows"]
                    path=re.split(r'/',z["path"])
                    path=path[0:-1]
                    for x in path:
                        u=u+"/"+x
                        mmkdir(downloadlocation+u)
                    download(z["url"],downloadlocation+"/"+z["path"])
        else:            
            o=o["downloads"]["artifact"]
            path=re.split(r'/',o["path"])
            path=path[0:-1]
            for x in path:
                u=u+"/"+x
                mmkdir(downloadlocation+u)
            download(o["url"],downloadlocation+"/"+o["path"])
def downloadminecraftasset(json,downloadlocation):
    mmkdir(downloadlocation)
    mmkdir(downloadlocation+"/indexes/")
    mmkdir(downloadlocation+"/objects/")
    downloada(json["url"],downloadlocation+"/indexes"+"/"+json["id"]+".json")
    file=open(downloadlocation+"/indexes"+"/"+json["id"]+".json")
    json=file.read()
    json=re.sub(r'(null)',"None",json)
    json=re.sub(r'(true)',"True",json)
    json=re.sub(r'(false)',"Flse",json)
    json=eval(json)
    json=json["objects"]
    for vls in json.values():
        hasha=vls["hash"]
        hasha2=hasha[0:2]
        mmkdir(downloadlocation+"/objects/"+"/"+hasha2+"/")
        q='https://download.mcbbs.net/assets/{:s}/{:s}'
        url=q.format(hasha2,hasha)
        u='{:s}/{:s}/{:s}'
        path=u.format(downloadlocation+"/objects/",hasha2,hasha)
        download(url,path)
    
 

    
    
    
            
    
#https://launchermeta.mojang.com/mc/game/version_manifest.json

