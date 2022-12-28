import os
import pathlib
from utils import exefinder, inputHandler,namespace
import executor
import appdirs
import json
import shutil

dir_=appdirs.user_data_dir("TShell","PStudio","1.2.7",True).replace("\\","/")
jSettings=dir_+"/settings"
jstartup=dir_+"/startup.tsh"
assetdir=dir_

if os.path.exists("./assets"):
    try:
        shutil.copytree("./assets",dir_+"/assets")
    except:pass

namespace.VARIABLES.update(
    {
        "TDIR":dir_,
        "PATH":os.environ["PATH"],
        "TSTARTUP":jstartup,
        "TASSET":assetdir+"/assets"
    }
)

if not os.path.exists(dir_):
    try:
        os.makedirs(dir_)
    except:pass

if not os.path.exists(jSettings):
    json.dump(namespace.VARIABLES,open(jSettings,"w"))
if not os.path.exists(jstartup):
    open(jstartup,"x")

namespace.VARIABLES.update(json.load(open(jSettings)))

handler=inputHandler.PromptInterface(additionalContentHistory=exefinder.allcommands())
exc=executor.executor(handler,namespace,assets=assetdir)

def format(r:str) -> str:
    for a,b in namespace.COSTANTS.items():
        r=r.replace("$"+a,str(b))
    for a,b in namespace.VARIABLES.items():
        r=r.replace("$"+a,str(b))
    return r

exc.execute(jstartup)

while True:
    try:
        input=handler.prompt(format(namespace.VARIABLES.get("FORMAT",">")))
        exc.execute(input)
    except KeyboardInterrupt:
        print("Interrupted...")
    except EOFError:
        print("Exit request received...")
        break
handler.saveall()