from datetime import datetime
import os,toml,platform,socket
import pathlib
from colorama import Back, Fore, Style,init
from os import getlogin as login
init(True)
GLOBALS = {}

def cwd():
    return os.getcwd().replace("\\","/").replace("/","")

COSTANTS = {
    "_": "\n",
    "$": "$",
    "A": "&",
    "B": "|",
    "D": datetime.now().strftime("%D"),
    "F": ")",
    "G": ">",
    "H": "~",
    "RH": pathlib.Path.home().absolute().__str__(),
    "I": login(),
    "J": socket.gethostname(),
    "L": "<",
    "N": f"{os.getcwd().split(':')[0]}",
    "M": f"{os.getcwd()}",
    "O": "{0}".format(os.getcwd().replace("\\", "/").split("/")[-1]) if not len(os.getcwd().replace("\\", "/").split("/"))==2 else os.getcwd().replace("\\", "/").split("/")[0]+"\\" if not pathlib.Path.home().absolute()==pathlib.Path(os.getcwd()).absolute() else "~",
    "RM": f"{cwd()}",
    "P": "=",
    "Q": " ",
    "S": datetime.now().strftime("%T"),
    "V": f"{platform.version()}",
    "CH0": "(",
    "CH1": "§",
    "CH2": "✓",
    "CH3": "✕",
    "CH4": "",
    "CH5": "✶",
    "CH6": "⌥",
    "CH7": "⌘",
    "CH8": "⏻",
    "CH9": "⏼",
    "CR1": "⎞",
    "CR2": "⎜",
    "CR3": "⎝",
    "CR4": "⎛",
    "CR5": "⎟",
    "CR6": "⎠",
    "CR7": "⭘",
    "CR8": "",
    "CR9": "",
}


VARIABLES={
    "FORMAT": f"""<p bg="ansiblue">$Q$CR9$Q</p><p bg="ansiyellow" fg="ansiblue">$CR8</p><p bg="ansiyellow">$Q$I@$J$Q</p><p bg="gray" fg="ansiyellow">$CR8</p><p bg="gray">$Q$O$Q</p><p fg="gray">$CR8</p>$Q""",
    "CWD": os.getcwd(),
    "HOME":pathlib.Path.home().absolute().__str__(),
}

ALIASES={
    "clear":"cls"
}

def update():
    VARIABLES.update({
        "CWD": f"{os.getcwd()}",
    })
    COSTANTS.update({
        "N": f"{os.getcwd().split(':')[0]}",
        "M": f"{os.getcwd()}",
        "RM": f"{cwd()}",
        "O": "{0}".format(os.getcwd().replace("\\", "/").split("/")[-1]) if not len(os.getcwd().replace("\\", "/").split("/"))==2 else os.getcwd().replace("\\", "/").split("/")[0]+"\\" if not pathlib.Path.home().absolute()==pathlib.Path(os.getcwd()).absolute() else "~",
        "S": datetime.now().strftime("%T"),
        "V": f"{platform.version()}",
    })

def formatStr(string:str) -> str:
    for a,b in COSTANTS.items():
        string=string.replace(a,b);
    return string;

def updateVariables(command:str,regex):
    try:
        if regex.match(command):
            VARIABLES.update(toml.loads(command))
            return True
    except:pass
    return False