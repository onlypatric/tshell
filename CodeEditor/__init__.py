from datetime import datetime
from tkinter import END, Menu, Text, Tk,N,E,W,S,BOTTOM,TOP,LEFT,RIGHT,X,Y,BOTH, filedialog, simpledialog;
from tkinter.ttk import *;
from PyQt5.QtWidgets import QApplication;
from PIL import Image, ImageTk,ImageOps
import pyperclip;
import sv_ttk as SetStyle
import os,sys,ctypes as ct,threading as thread,darkdetect as d,idlelib.colorizer as ic,idlelib.percolator as ip,re;

class App:
# -------------------------- INITIALIZE APPLICATION
    def __init__(self,directory:str=".",args=sys.argv) -> None:
        self.args=args
        if((len(self.args))>1 or not __file__.endswith((".py",".pyw"))and not "--light" in self.args):
            self.path=self.args[-1]
            if not os.path.exists(self.path):
                open(self.path,"a+",encoding="utf8").close()
        else:
            self.path=None

        self.fontSize=12;
        self.codeActive=False;
        self.ip=None;
        self.directory=directory;
        QApplication(self.args)
        self.thread=thread.Thread(target=self.main)
    def updateTitle(self,*args) -> None:
        self.root.title(f"*{self.path} - WEdit")
# -------------------------- SAVE FILE HANDLER

    def save(self,*args):
        try:
            if self.path is None:
                self.saveas()
                return;
            open(self.path,"w",encoding="utf8").write(self.notepad.get("1.0","end-1c"))
            self.root.title(f"{self.path} - WEdit")
        except:pass    
    def saveas(self,*args):
        try:
            self.path=filedialog.asksaveasfilename(filetypes=[("Text file",".txt"),("Any file",".*"),("C source",".c"),("C++ source",".cpp"),("Java source",".java"),("JavaScript source",".js"),("TypeScript source",".ts"),("HTML source",".html"),("CSS source",".css"),("Assembly source",".asm"),("Python source",".py"),("Python consoleless source",".pyw"),],parent=self.root,title="save file",initialfile="untilted.txt").replace("\\","/")
            if self.path is not None:
                if self.path.endswith((".pyw","py",".c","cpp",".js",".java",".ts",".go",".asm",".h",".hpp",".html",".htm",".css")):
                    if not self.codeActive:self.syntaxSetter()
                self.save()
        except:pass
    
    def importfile(self,*args):
        try:
            path=filedialog.askopenfilename(filetypes=[("Text file",".txt"),("Any file",".*"),("C source",".c"),("C++ source",".cpp"),("Java source",".java"),("JavaScript source",".js"),("TypeScript source",".ts"),("HTML source",".html"),("CSS source",".css"),("Assembly source",".asm"),("Python source",".py"),("Python consoleless source",".pyw"),],parent=self.root,title="import file").replace("\\","/")
            if path is not None:
                if path.endswith((".pyw","py",".c","cpp",".js",".java",".ts",".go",".asm",".h",".hpp",".html",".htm",".css")):
                    if not self.codeActive:self.syntaxSetter()
                self.notepad.insert(END,path)
        except:pass    
    
    def open(self,new:bool=False,*args):
        try:
            self.path=filedialog.askopenfilename(filetypes=[("Text file",".txt"),("Any file",".*"),("C source",".c"),("C++ source",".cpp"),("Java source",".java"),("JavaScript source",".js"),("TypeScript source",".ts"),("HTML source",".html"),("CSS source",".css"),("Assembly source",".asm"),("Python source",".py"),("Python consoleless source",".pyw"),],parent=self.root,title="open file").replace("\\","/")
            if self.path is not None:
                if self.path.endswith((".pyw","py",".c","cpp",".js",".java",".ts",".go",".asm",".h",".hpp",".html",".htm",".css")):
                    if not self.codeActive:self.syntaxSetter()
                self.notepad.delete("1.0",END)
                self.notepad.insert(END,open(self.path,"r",encoding="utf8").read())
                self.save()
        except:pass
# -------------------------- SYNTAX HIGHLIGHTING STUFF
    def syntaxSetter(self,*args,**kwargs):
        KEYWORD   = r"\b(?P<KEYWORD>False|None|True|true|false|public|static|and|as|assert|void|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b"
        EXCEPTION = r"([^.'\"\\#]\b|^)(?P<EXCEPTION>ArithmeticError|AssertionError|AttributeError|BaseException|BlockingIOError|BrokenPipeError|BufferError|BytesWarning|ChildProcessError|ConnectionAbortedError|ConnectionError|ConnectionRefusedError|ConnectionResetError|DeprecationWarning|EOFError|Ellipsis|EnvironmentError|Exception|FileExistsError|FileNotFoundError|FloatingPointError|FutureWarning|GeneratorExit|IOError|ImportError|ImportWarning|IndentationError|IndexError|InterruptedError|IsADirectoryError|KeyError|KeyboardInterrupt|LookupError|MemoryError|ModuleNotFoundError|NameError|NotADirectoryError|NotImplemented|NotImplementedError|OSError|OverflowError|PendingDeprecationWarning|PermissionError|ProcessLookupError|RecursionError|ReferenceError|ResourceWarning|RuntimeError|RuntimeWarning|StopAsyncIteration|StopIteration|SyntaxError|SyntaxWarning|SystemError|SystemExit|TabError|TimeoutError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError|Warning|WindowsError|ZeroDivisionError)\b"
        BUILTIN   = r"([^.'\"\\#]\b|^)(?P<BUILTIN>abs|printf|scanf|cout|cin|System|println|mov|all|any|ascii|bin|breakpoint|callable|chr|classmethod|compile|complex|copyright|credits|delattr|dir|divmod|enumerate|eval|exec|exit|filter|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|isinstance|issubclass|iter|len|license|locals|map|max|memoryview|min|next|oct|open|ord|pow|print|quit|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|sum|type|vars|zip)\b"
        DOCSTRING = r"(?P<DOCSTRING>(?i:r|u|f|fr|rf|b|br|rb)?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?|(?i:r|u|f|fr|rf|b|br|rb)?\"\"\"[^\"\\]*((\\.|\"(?!\"\"))[^\"\\]*)*(\"\"\")?)"
        STRING    = r"(?P<STRING>(?i:r|u|f|fr|rf|b|br|rb)?'[^'\\\n]*(\\.[^'\\\n]*)*'?|(?i:r|u|f|fr|rf|b|br|rb)?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
        TYPES     = r"\b(?P<TYPES>bool|bytearray|bytes|dict|float|int|list|str|tuple|object|char|double)\b"
        NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
        CLASSDEF  = r"(?<=\bclass)[ \t]+(?P<CLASSDEF>\w+)[ \t]*[:\(]" #recolor of DEFINITION for class definitions
        DECORATOR = r"(^[ \t]*(?P<DECORATOR>@[\w\d\.]+))"
        INSTANCE  = r"\b(?P<INSTANCE>super|self|cls)\b"
        COMMENT   = r"(?P<COMMENT>#|//[^\n]*)"
        SYNC      = r"(?P<SYNC>\n)"
        PROG   = rf"{KEYWORD}|{BUILTIN}|{EXCEPTION}|{TYPES}|{COMMENT}|{DOCSTRING}|{STRING}|{SYNC}|{INSTANCE}|{DECORATOR}|{NUMBER}|{CLASSDEF}"
        IDPROG = r"(?<!class)\s+(\w+)"
        TAGDEFS   = {   'COMMENT'    : {'foreground': '#333333',    'background': None},
                        'TYPES'      : {'foreground': '#c70a0a',    'background': None},
                        'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                        'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                        'STRING'     : {'foreground': '#28b9c9',    'background': None},
                        'DOCSTRING'  : {'foreground': '#28b9c9',    'background': None},
                        'EXCEPTION'  : {'foreground': '#e00914',    'background': None},
                        'DEFINITION' : {'foreground': '#44ab1b',    'background': None},
                        'DECORATOR'  : {'foreground': '#994f2c',    'background': None},
                        'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                        'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        'CLASSDEF'   : {'foreground': '#c97f1e',    'background': None},
                    }
        cd         = ic.ColorDelegator()
        cd.prog    = re.compile(PROG, re.S|re.M)
        cd.idprog  = re.compile(IDPROG, re.S)
        cd.tagdefs = {**cd.tagdefs, **TAGDEFS}
        if self.ip is None:
            self.ip=ip.Percolator(self.notepad)

        if self.codeActive:
            cd.tagdefs = {   'COMMENT'    : {'foreground': '#FFF',    'background': None},
                        'TYPES'      : {'foreground': '#FFF',    'background': None},
                        'NUMBER'     : {'foreground': '#FFF',    'background': None},
                        'BUILTIN'    : {'foreground': '#FFF',    'background': None},
                        'STRING'     : {'foreground': '#FFF',    'background': None},
                        'DOCSTRING'  : {'foreground': '#FFF',    'background': None},
                        'EXCEPTION'  : {'foreground': '#FFF',    'background': None},
                        'DEFINITION' : {'foreground': '#FFF',    'background': None},
                        'DECORATOR'  : {'foreground': '#FFF',    'background': None},
                        'INSTANCE'   : {'foreground': '#FFF',    'background': None},
                        'KEYWORD'    : {'foreground': '#FFF',    'background': None},
                        'CLASSDEF'   : {'foreground': '#FFF',    'background': None},
                    }
        self.ip.insertfilter(cd)
        self.codeActive = not self.codeActive
# -------------------------- DARK TITLE BAR
    def darkTitleBar(self):
        """
        MORE INFO:
        https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
        """
        try:
            self.root.update()
            if os.name=="nt":
                ct.windll.dwmapi.DwmSetWindowAttribute(
                    ct.windll.user32.GetParent(
                        self.root.winfo_id()
                    ), 
                    20, 
                    ct.byref(
                        ct.c_int(2)
                    ),
                    ct.sizeof(
                        ct.c_int(2)
                    )
                )
        except:pass
# -------------------------- START APP
    def start(self):
        self.thread.start();
# -------------------------- CLOSE APP
    def close(self,*args,**kwargs):
        if self.path is not None:
            self.save()
        self.root.withdraw();
        sys.exit(0);
# -------------------------- NEGATIVIZE COLORS OF ANY IMAGE
    def invert(self,image:Image.Image):
        if image.mode == 'RGBA':
            r,g,b,a = image.split()
            rgb_image = Image.merge('RGB', (r,g,b))

            inverted_image = ImageOps.invert(rgb_image)

            r2,g2,b2 = inverted_image.split()

            final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))

            return final_transparent_image
        else:
            inverted_image = ImageOps.invert(image)
            return inverted_image
    def increaseFont(self,*args,**kwargs):
        self.fontSize+=1
        self.notepad.configure(font=f"Courier {self.fontSize}")
    def decreaseFont(self,*args,**kwargs):
        if self.fontSize<5:
            return;
        self.fontSize-=1
        self.notepad.configure(font=f"Courier {self.fontSize}")
# -------------------------- CONFIGURE ROOT SETTINGS AND PROPERTIES
    def configure(self):
        self.root.protocol("WM_DELETE_WINDOW",self.close)#Protocol for closing
        self.root.bind("<Control-w>",self.close)#Shortcut (like exporer or google chrome)
        self.root.bind("<Control-+>",self.increaseFont)
        self.root.bind("<Control-minus>",self.decreaseFont)
        self.root.bind("<Control-s>",self.save)
        self.root.bind("<Control-Shift-S>",self.saveas)
        self.root.bind("<Control-o>",self.open)
        self.root.bind("<Control-Shift-O>",self.importfile)
        self.root.bind("<Control-t>",self.timeIn)
        self.root.bind("<Key>",self.updateTitle)
        

        #root size
        self.root.geometry("%dx%d"%(self.root.winfo_screenwidth()/2.5,self.root.winfo_screenheight()/2.5))
        
        #title
        self.root.title("Untilted - WEdit")

        #upscale to 2x
        self.root.tk.call('tk', 'scaling',2)
        
        #set dark theme things (icons,theme)
        if d.isDark() and "--light" not in self.args:
            self.darkTitleBar()
            SetStyle.set_theme("dark")
            self.images={
                "open":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/open.png")).resize([20,20])),
                "file":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/menu.png")).resize([20,20])),
                "save":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/save.png").resize([20,20]))),
                "saveas":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/saveas.png").resize([20,20]))),
                "add":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/add.png").resize([20,20]))),
                "find":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/find.png").resize([20,20]))),
                "findnext":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/findnext.png").resize([20,20]))),
                "findprev":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/findprev.png").resize([20,20]))),
                "redo":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/redo.png").resize([20,20]))),
                "undo":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/undo.png").resize([20,20]))),
                "copy":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/copy.png").resize([20,20]))),
                "cut":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/cut.png").resize([20,20]))),
                "delete":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/delete.png").resize([20,20]))),
                "goto":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/goto.png").resize([20,20]))),
                "select":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/select.png").resize([20,20]))),
                "date":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/date.png").resize([20,20]))),
                "code":ImageTk.PhotoImage(self.invert(Image.open(f"{self.directory}/assets/code.png").resize([20,20]))),
            }
        else:
            self.images={
                "open":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/open.png").resize([20,20])),
                "file":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/menu.png").resize([20,20])),
                "save":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/save.png").resize([20,20])),
                "saveas":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/saveas.png").resize([20,20])),
                "add":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/add.png").resize([20,20])),
                "find":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/find.png").resize([20,20])),
                "findnext":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/findnext.png").resize([20,20])),
                "findprev":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/findprev.png").resize([20,20])),
                "redo":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/redo.png").resize([20,20])),
                "undo":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/undo.png").resize([20,20])),
                "copy":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/copy.png").resize([20,20])),
                "cut":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/cut.png").resize([20,20])),
                "delete":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/delete.png").resize([20,20])),
                "goto":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/goto.png").resize([20,20])),
                "select":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/select.png").resize([20,20])),
                "date":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/date.png").resize([20,20])),
                "code":ImageTk.PhotoImage(Image.open(f"{self.directory}/assets/code.png").resize([20,20])),
            }
            SetStyle.set_theme("light")
# -------------------------- DATETIME
    def timeIn(self, *args):
        self.notepad.insert(END,"%s\n"%(datetime.now().strftime("%D %T")))
# -------------------------- CUT TEXT
    def cut(self):
        pyperclip.copy(self.notepad.selection_get())
        self.notepad.selection_clear()
    def undo(self):
        self.notepad.edit_undo()
    def redo(self):
        self.notepad.edit_redo()
# -------------------------- TOP MENU BAR BUILT FROM SCRATCH
    def menubar(self):
        self.topbar=Frame(self.root)
        self.topbar.pack(side=TOP,fill=X)


        self.menu1=Menu(self.root)
        self.menu1.add_command(label="Open",accelerator="Ctrl+O",underline=0,image=self.images.get("open"),command=self.open,compound="left")
        self.menu1.add_command(label="Import text",accelerator="Ctrl+Shift+O",underline=0,image=self.images.get("add"),command=self.importfile,compound="left")
        self.menu1.add_separator()
        self.menu1.add_command(label="Save",accelerator="Ctrl+S",underline=0,image=self.images.get("save"),command=self.save,compound="left")
        self.menu1.add_command(label="Save As",accelerator="Ctrl+Shift+S",underline=0,image=self.images.get("saveas"),command=self.saveas,compound="left")
        
        self.MenuButton1=Menubutton(self.topbar,text="File",menu=self.menu1,image=self.images.get("file"),compound="left")
        self.MenuButton1.pack(side=LEFT)

        self.menu2=Menu(self.root)
        self.root.bind("<Control-Shift-C>",self.syntaxSetter)
        self.menu2.add_command(label="Code Highlighting",accelerator="Ctrl+Shift+C",command=self.syntaxSetter,underline=0,image=self.images.get("code"),compound="left")
        self.menu2.add_separator()
        self.menu2.add_command(label="Find",accelerator="Ctrl+F",underline=0,image=self.images.get("find"),compound="left")
        self.menu2.add_command(label="Find Next",accelerator="Ctrl+Shift+F",underline=0,image=self.images.get("findnext"),compound="left")
        self.menu2.add_command(label="Find Previous",accelerator="Ctrl+Alt+F",underline=0,image=self.images.get("findprev"),compound="left")
        self.menu2.add_command(label="Go to",accelerator="Ctrl+G",underline=0,image=self.images.get("goto"),compound="left")
        self.menu2.add_separator()
        self.menu2.add_command(label="Undo",accelerator="Ctrl+Z",command=self.undo,underline=0,image=self.images.get("undo"),compound="left")
        self.menu2.add_command(label="Redo",accelerator="Ctrl+Y",command=self.redo,underline=0,image=self.images.get("redo"),compound="left")
        self.menu2.add_separator()
        self.menu2.add_command(label="Copy",accelerator="Ctrl+C",command=lambda:pyperclip.copy(self.notepad.selection_get()),underline=0,image=self.images.get("copy"),compound="left")
        self.menu2.add_command(label="Cut",accelerator="Ctrl+X",command=self.cut,underline=0,image=self.images.get("cut"),compound="left")
        self.menu2.add_command(label="Select all",accelerator="Ctrl+A",underline=0,image=self.images.get("select"),compound="left")
        self.menu2.add_command(label="Delete",accelerator="Canc",underline=0,image=self.images.get("delete"),compound="left")

        self.MenuButton2=Menubutton(self.topbar,text="Modify",menu=self.menu2,image=self.images.get("file"),compound="left")
        self.MenuButton2.pack(side=LEFT)

        self.menu3=Menu(self.root)
        self.menu3.add_command(label="Date and Time",command=self.timeIn,accelerator="Ctrl+T",underline=0,image=self.images.get("date"),compound="left")

        self.MenuButton3=Menubutton(self.topbar,text="Insert",menu=self.menu3,image=self.images.get("file"),compound="left")
        self.MenuButton3.pack(side=LEFT)

        self.root.update()
    
    def get(self,arr,key):
        try:
            return arr[key]
        except:
            return "";
    
    def indent(self,*args,**kwargs):
        # kinda buggy for now not implemented
        # if self.codeActive:
        #     o_=self.notepad.get("1.0","end-1c")
        #     o2_=self.get(o_.splitlines(),-1)
        #     self.notepad.insert(END,"\t"*o2_.count("\t"))
        #     self.notepad.update()
        #     return
        return

    def textbox(self):
        self.notepad=Text(self.root,font=f"Courier {self.fontSize}",maxundo=-1,undo=True)
        self.notepad.pack(side=TOP,fill=BOTH,expand=True)
        self.notepad.bind("<Return>",self.indent)
    def main(self):
        self.root=Tk();

        self.configure();

        self.menubar();

        self.textbox();

        #Some bottom colorings (win only)
        Progressbar(self.root,value=100).pack(side=BOTTOM)

        self.root.mainloop();

if __name__=="__main__":
    app=App()
    app.start()