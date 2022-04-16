import json
import zipfile
import os
def mmkdir(path):
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
def _cp(ida,gameDir):
    lista=[]
    a=open(gameDir+"versions/"+ida+"/"+ida+".json","r")
    a=json.load(a)
    a=a["libraries"]
    lista.append(gameDir+"versions/"+ida+"/"+ida+".jar") 
    for i in range(len(a)):
        o=a[i]
        if "artifact" in o["downloads"]:
            o=o["downloads"]["artifact"]
            o=o["path"]
        else:
            continue
        lista.append(gameDir+"libraries/"+o)
    c="-cp "
    for i in range(len(lista)):
        c=c+lista[i]+";"
    c=c[0:(len(c)-1)]
    return c
def jardecompression(DecompressionDir,gameDir,ida):
    y=open(gameDir+"versions/"+ida+"/"+ida+".json","r")
    y=json.load(y)
    y=y["libraries"]
    for i in range(len(y)):
        if "classifiers" in y[i]["downloads"]:
            ia=y[i]["downloads"]["classifiers"]
            if "natives-windows" in ia:
                ia=ia["natives-windows"]
                extracting = zipfile.ZipFile(gameDir+"libraries/"+ia["path"])
                extracting.extractall(DecompressionDir)
def run_minecraft(ida,gameDir,javadir,xmn,xmx,natives,LunchVersion,AssetsDir,UserName,AssetIndex,token,uuid):
    o=open(gameDir+"versions/"+ida+"/"+ida+".json","r")
    o=json.load(o)
    cp=_cp(ida,gameDir)
    jardecompression(natives,gameDir,ida)
    StartupParameter=javadir+" -Dminecraft.client.jar="+gameDir+"versions/"+ida+"/"+ida+".jar "
    StartupParameter=StartupParameter+cp+" -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=16m -XX:-UseAdaptiveSizePolicy -XX:-OmitStackTraceInFastThrow -XX:-DontCompileHugeMethods"+" -Xmn"+xmn+"m -Xmx"+xmx+"m -Dfml.ignoreInvalidMinecraftCertificates=true -Dfml.ignorePatchDiscrepancies=true -XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump "
    StartupParameter=StartupParameter+" -Djava.library.path="+natives+" -Dminecraft.launcher.brand=minecraft-launcher -Dminecraft.launcher.version="+LunchVersion
    StartupParameter=StartupParameter+" "+o["mainClass"]
    StartupParameter=StartupParameter+" --width 854 --height 480"+" --userType legacy "+" --versionType "+ida+" --assetsDir "+AssetsDir+" --gameDir "+gameDir+" --username "+UserName+" --assetIndex "+AssetIndex+" --version "+ida
    StartupParameter=StartupParameter+" --accessToken "+token
    StartupParameter=StartupParameter+" --uuid "+uuid
    print(StartupParameter)
    os.popen(StartupParameter)
run_minecraft("1.12.2","D:/.minecraft/","javaw","128","2048","D:\.minecraft/versions/1.12.2/natives","1.12.2","D:\.minecraft/assets","zxz","1.12.2","000","0")
