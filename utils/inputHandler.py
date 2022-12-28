import os,atexit,json,pathlib,sys
from colorama import Back, Fore,Style as ColStyle
from pygments.lexers.shell import PowerShellLexer
from prompt_toolkit import prompt,HTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import style
from prompt_toolkit.lexers import PygmentsLexer

class PromptInterface:
    def is_multiline(self,document):
        # Get the current line of the document
        current_line = document.current_line

        # Check if the current line contains an opening curly brace
        if "{" in current_line:
            # If the current line contains an opening curly brace, check if the line
            # also contains a closing curly brace
            if "}" in current_line:
                # If the current line contains both an opening and closing curly brace,
                # the prompt should not be in multiline mode
                return False
            else:
                # If the current line contains only an opening curly brace, the prompt
                # should be in multiline mode
                return True
        else:
            # If the current line does not contain an opening curly brace, the prompt
            # should not be in multiline mode
            return False
    def __init__(self,pathWhereToSave:str=pathlib.Path.home().absolute().__str__(),additionalContentHistory:"list[str]"=[],save:bool=True) -> None:
        #Path checking just in case
        if os.path.isdir(pathWhereToSave):
            pathWhereToSave=pathWhereToSave+"\\.tshistory"
            if not os.path.exists(pathWhereToSave.replace("\\","/")):
                json.dump({"history":[]},open(pathWhereToSave,"w"))
        #Load initial history
        try:
            self.historyStrings:"list[str]"=list(dict.fromkeys(json.load(open(pathWhereToSave))["history"]))
        except:
            json.dump({"history":[]},open(pathWhereToSave,"w"))
            self.historyStrings:"list[str]"=json.load(open(pathWhereToSave))["history"]
        [self.historyStrings.insert(0,i) for i in additionalContentHistory]
        self.history = InMemoryHistory(self.historyStrings)
        self.pathWhereToSave=pathWhereToSave
        self.save=save
        atexit.register(self.saveall)

    def saveall(self):
        json.dump({"history":self.history.get_strings()},open(self.pathWhereToSave,"w"))

    def prompt(self,prompt_:str=""):

        #Current dir
        files = [f"./{i}" for i in os.listdir()]

        #Generate this because sum of lists somehow doesnt work.
        tempHistory=[]
        #Append current dir
        tempHistory.extend(files)
        #Append history files
        tempHistory.extend(self.history.get_strings())

        completer = WordCompleter(tempHistory, ignore_case=True, WORD=True)
        _style = style.Style.from_dict({
            'pygments.keyword': 'underline',
            'pygments.literal.string': 'bg:#00ff00 #ffffff',
        })
        text = prompt(HTML(prompt_),lexer=PygmentsLexer(PowerShellLexer),auto_suggest=AutoSuggestFromHistory(),complete_in_thread=True,style=_style,mouse_support=True,complete_while_typing=True,completer=completer,history=self.history).strip()

        if self.save:
            self.history.store_string(text)
            self.saveall()

        return text

if __name__=="__main__":
    prompt_=PromptInterface()
    while True:
        prompt_.prompt(">>>")