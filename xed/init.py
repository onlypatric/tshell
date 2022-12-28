import os,sys

from colorama import init,Back,Fore

init(autoreset=True)

try:
    from AP import FindParams,FindSettings
except:
    from .ObjParser import FindParams, FindSettings

class argvParser:
    def __init__(self,initialOptions:"dict[str,str|bool]"={},argv:"list[str]"=sys.argv) -> None:
        self.argv=" ".join(argv)
        self.listargv=argv
        self.options={}
        self.params=FindParams(self.argv)
        self.settings=FindSettings(self.argv)
        for i in self.settings:
            self.add(name=i,default=self.settings[i]["value"])
        self.options.update(initialOptions)
    def add(self,
        name:str=None,
        default:str=None,
        help:str=f"{Back.RED}Undocumented/Not existent{Back.RESET}",
    ):
        if self.options.get(name,None) == None:
            self.options[name]={
                "value":default
            }
        self.options[name]["help"]=help
    def __str__(self) -> str:
        return "Options:"+str(["--"+i for i in self.settings])+"\nParameters provided:"+str(self.params)
    def GetOption(self,name:str=None,default:str=False):
        return self.options.get(name,{"value":default})["value"]
    def GetArgs(self):
        return self.params
    def help(self):
        r="\n".join(["\t--%-15s-\t%10s"%(_,a["help"]) for _,a in self.options.items()])
        return r
import curses,sys
import os
from .x_editor import Editor
from colorama import Fore

def showHelp():
    help_txt = (f" Save and exit         {Fore.CYAN}:{Fore.RESET} F2 or Ctrl-x\n"
                f"            (Enter if in single-line entry mode)\n"
                f" Exit (no save)        {Fore.CYAN}:{Fore.RESET} F3, Ctrl-c or ESC\n"
                f" Cursor movement       {Fore.CYAN}:{Fore.RESET} Arrow keys/Ctrl-f/b/n/p\n"
                f" Beginning of line     {Fore.CYAN}:{Fore.RESET} Home/Ctrl-a\n"
                f" End of line           {Fore.CYAN}:{Fore.RESET} End/Ctrl-e\n"
                f" Page Up/Page Down     {Fore.CYAN}:{Fore.RESET} PgUp/PgDn\n"
                f" Backspace/Delete      {Fore.CYAN}:{Fore.RESET} Backspace/Ctrl-h\n"
                f" Delete current char   {Fore.CYAN}:{Fore.RESET} Del/Ctrl-d\n"
                f" Insert line at cursor {Fore.CYAN}:{Fore.RESET} Enter\n"
                f" Paste block of text   {Fore.CYAN}:{Fore.RESET} Ctrl-v\n"
                f" Delete to end of line {Fore.CYAN}:{Fore.RESET} Ctrl-k\n"
                f" Delete to BOL         {Fore.CYAN}:{Fore.RESET} Ctrl-u\n")
    help_txt_no = (
                f" Quit                  {Fore.CYAN}:{Fore.RESET} q,F2,F3,ESC,Ctrl-c or Ctrl-x\n"
                f" Cursor movement       {Fore.CYAN}:{Fore.RESET} Arrow keys/j-k/Ctrl-n/p\n"
                f" Page Up/Page Down     {Fore.CYAN}:{Fore.RESET} J/K/PgUp/PgDn/Ctrl-b/n\n")
    sys.stdout.write(help_txt)
    sys.stdout.write("\n\tFor read only mode:\n\n")
    sys.stdout.write(help_txt_no)

class _Editor:
    def __init__(self,fName:"str|None"=None,settings:"dict[str,str]"={}) -> None:
        self.size=(20,80)
        self.settings=settings
        self.lines=int(self.settings.get("lines",0)) if str(self.settings.get("lines",0)).isdigit() else 0
        try:
            self.size=(os.get_terminal_size().lines,os.get_terminal_size().columns)
        except:pass
        if fName==None:
            fName="untilted.txt"
        self.fName=fName
        if not os.path.exists(self.fName):
            try:
                open(self.fName,"x")
            except:
                self.fName="untilted.txt"
                open(self.fName,"x")
        self.textDefault=open(self.fName,"r").read()
        self.fName=fName
        curses.wrapper(self.main)

    def main(self,stdscr):
        self.editor=Editor(stdscr,max_paragraphs=self.lines,inittext=self.textDefault,edit=not (self.settings.get("r",False) or self.settings.get("read",False)),box=(self.settings.get("b",False) or self.settings.get("box",False)),title="XEditor",win_size=self.size,win_location=(5,5),save=self.save)
        try:
            self.editor()
        except KeyboardInterrupt:pass
        except:pass
        self.save()

    def save(self):
        try:
            if not os.path.exists(self.fName):
                try:
                    open(self.fName,"x")
                except:
                    self.fName="untilted.txt"
                    open(self.fName,"x")
            open(self.fName,"w").write(self.getText())
        except Exception as e:
            print(e)
    def getText(self):
        r="\n".join([i for i in ["".join(j) for j in self.editor.text]])

        return r
def get(arr,idx,def_):
    try:
        return arr[idx]
    except Exception as e:
        return def_

if __name__=="__main__":
    commandArgs=argvParser()
    commandArgs.params.pop(0)
    if commandArgs.settings.get("h",False) or commandArgs.settings.get("help",False):
        showHelp()
    else:
        _Editor(get(commandArgs.GetArgs(),-1,"untilted.txt"),commandArgs.settings)
def start(args=sys.argv):
    commandArgs=argvParser(argv=args)
    commandArgs.params.pop(0)
    if commandArgs.settings.get("h",False) or commandArgs.settings.get("help",False):
        showHelp()
    else:
        _Editor(get(commandArgs.GetArgs(),0,"untilted.txt"),commandArgs.settings)