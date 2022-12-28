import os
import pathlib
import re
import shutil
import subprocess
import traceback
import browser
import sys
import colorama as c
import xed.init
import ast
import appdirs
import CodeEditor
from io import StringIO
from numerize import numerize
from decimal import Decimal
from utils.exefinder import allcommands

from pyvim.entry_points.run_pyvim import run

def execute_code(code: str) -> str:
    code = add_global_to_variables(code)
    """Executes the given code and returns its output as a string."""
    # Redirect the standard output to a string buffer
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    # Execute the code
    exec(code)

    # Retrieve the output from the string buffer
    output = sys.stdout.getvalue()

    # Reset the standard output
    sys.stdout = old_stdout

    return output

def is_valid_python_code(code):
    try:
        # Parse the code string into an AST
        ast.parse(code)
        # If the code was successfully parsed, return True
        return True
    except SyntaxError:
        # If a SyntaxError was raised, the code is invalid, so return False
        return False

def add_global_to_variables(code) -> str:
    # Parse the code string into an AST
    tree = ast.parse(code,type_comments=True)

    # Iterate over the top-level nodes in the AST
    for node in tree.body:
        # Check if the node is an assignment statement
        if isinstance(node, ast.Assign):
            # Iterate over the target nodes in the assignment statement
            for target in node.targets:
                # Check if the target is a Name node (i.e. a variable)
                if isinstance(target, ast.Name):
                    # If the target is a variable, add the global statement
                    code = f"global {target.id}; {code}"
                    break
    
    # Return the modified code
    return code

import re

def find_content_between_parentheses(string):
    # Define the regular expression pattern
    pattern = r"\$\(((?:[^$]|\$(?!\())*)\)"

    # Find all the occurrences of the pattern in the string
    matches = re.findall(pattern, string)

    # Return the list of matches
    return matches



shXecutePattern=re.compile(r"^\$\s*\(\s*(.*?)\s*\)")
pyXecutePattern=re.compile(r"^\@\s*\{\s*(.*?)\s*\}")

def get_folder_size(folder_path):
    total_size = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)

    return total_size

def MakeCommandReadable(s):
    # Initialize an empty list to store the split strings
    split_strings = []
    # Initialize an empty string to build up the current split string
    current_split_string = ''
    # Initialize a flag to track whether the current character is inside double quotes
    in_quotes = False

    # Iterate through each character in the string
    for i, c in enumerate(s):
        # If we encounter a double quote character, toggle the in_quotes flag
        if c == '"':
            current_split_string += c
            in_quotes = not in_quotes
        # If we encounter a semicolon and we're not in quotes, split the string
        elif c == ';' and not in_quotes:
            split_strings.append(current_split_string)
            current_split_string = ''
        # Otherwise, add the character to the current split string
        else:
            current_split_string += c

    # Add the final split string to the list
    split_strings.append(current_split_string)

    return split_strings

def arrGet(arr,idx,default="."):
    try:
        return arr[idx]
    except:
        return default

def printPath(path:str):
    print(c.Back.GREEN+f"  ".join([i for i in os.getcwd().replace("\\","/").split("/")])+f" {c.Back.RESET}{c.Fore.GREEN}{c.Fore.RESET}")

def get_single_hyphen_params(string):
    # Extract all substrings that start with a single hyphen
    return re.findall(r'\b-\S*\b', string)
def get_double_hyphen_params(string):
    # Extract all substrings that start with two hyphens
    return re.findall(r'\b--\S*\b', string)
def get_fancy_params(string):
    # Extract all words that start with a forward slash or an at symbol
    return re.findall(r'\b[/@]\S*', string)
def get_string(string):
    # Extract all words that do not start with a hyphen, a forward slash, or an at symbol
    return re.findall(r'\b(?!-)(?![/@])\S*', string)
def get_params(string) -> "tuple[list[str],list[str]]":
    return (get_string(string),get_single_hyphen_params(string)+get_double_hyphen_params(string)+get_fancy_params(string))

def is_not_param(string):
    # Check if the string does not start with a hyphen
    return not re.match(r'^-', string)
variableAssignRegex = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*=")
variableCancelRegex = re.compile(r"^del\s+\S+$")

class executor:
    def __init__(self,handler,namespace,assets=".") -> None:
        self.assets=assets
        self.handler=handler
        self.namespace=namespace
        self.allcommands=allcommands()
    def format(self,r:str) -> str:
        for a,b in self.namespace.COSTANTS.items():
            r=r.replace("$"+a,str(b))
        for a,b in self.namespace.VARIABLES.items():
            r=r.replace("$"+a,str(b))
        for a,b in self.namespace.ALIASES.items():
            r=r.replace(a,str(b),1) if r.startswith(a) else r
        return r
    def SimpleFormat(self,r:str) -> str:
        for a,b in self.namespace.ALIASES.items():
            r=r.replace(a,str(b),1) if r.startswith(a) else r
        for a,b in self.namespace.VARIABLES.items():
            r=r.replace("$"+a,str(b))
        return r
    
    def execute(self,commandList:str):
        for script in pyXecutePattern.findall(commandList):
            try:
                commandList=commandList.replace("@{"+script+"}",execute_code(script))
            except Exception as e:
                print(traceback.format_exc())
        
        for shScript in find_content_between_parentheses(commandList):
            try:
                commandList="\""+commandList.replace(f"$({shScript})",subprocess.run(f"cmd /c {shScript}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8",errors="ignore"))+"\""
            except Exception as e:
                print(traceback.format_exc())
        for r in MakeCommandReadable(commandList):
            self.handler.historyStrings.append(r)
            if not self.namespace.updateVariables(r,variableAssignRegex):
                if r.startswith("exit"):
                    self.handler.saveall()
                    sys.exit(0)
                elif variableCancelRegex.match(r):
                    try:
                        self.namespace.VARIABLES.pop(r.replace("del ","",1))
                    except:
                        os.system(f"cmd /c {r}")
                    continue
                r=self.SimpleFormat(r)
                if self.is_valid_expression(r):
                    try:
                        res=eval(r,globals(),locals())
                        if res is not None:
                            print(res)
                    except:
                        os.system(f"cmd.exe /c {r}")
                elif r.startswith("printvar"):
                    print(self.namespace.VARIABLES)
                elif r.startswith("cd"):
                    if r.split().__len__()==1:
                        printPath(os.getcwd())
                    else:
                        try:
                            os.chdir(self.format([i for i in r.split()[1:] if is_not_param(i)][-1]))
                        except:
                            os.chdir(self.format("$RH"))
                    continue
                elif r.startswith("rmtree"):
                    if r.split().__len__()==1:
                        print("please specify a path.")
                    else:
                        try:
                            if "-a" in r or input(f"Proceed with deleting entire folder {r.replace('rm ','')} and all of its contents? (y/n)").lower()=="y":
                                shutil.rmtree(self.format([i for i in r.replace("-a","").split()[1:] if is_not_param(i)][-1]),ignore_errors=True)
                        except Exception as e:
                            print(e)
                            print("invalid path or permission denied...")
                    continue
                elif r.startswith("rm "):
                    if r.split().__len__()==1:
                        print("please specify a file.")
                    else:
                        try:
                            if "-a" in r or input(f"Proceed with deleting file {r.replace('rm ','')}? (y/n)").lower()=="y":
                                os.remove(self.format([i for i in r.replace("-a","").split()[1:] if is_not_param(i)][-1]))
                        except Exception as e:
                            print(e)
                            print("invalid file or permission denied...")
                    continue
                elif r=="tb" or r=="browser":
                    try:
                        browser.app()
                    except:pass
                    os.system("cls")
                elif r.startswith("vim"):
                    try:
                        rgs=r.split()
                        rgs.pop(0) # removes "vim"
                        run(args=rgs)
                    except:pass
                elif r.startswith("xe"):
                    if "-c" in r or "--console" in r:
                        r=r.replace("-c","",1)
                        xed.init.start(r.split())
                    else:
                        ap=CodeEditor.App(directory=self.assets,args=r.split())
                        ap.start()
                elif r.startswith(("dir","ls")):
                    a=r.split()
                    a.pop(0)
                    params,settings=get_params(" ".join(a))
                    path=arrGet(params,0) if os.path.exists(arrGet(params,0)) and os.path.isdir(arrGet(params,0)) else "."
                    fileList=os.listdir(path)
                    print(settings)
                    mx=max([len(i) for i in fileList])
                    print()
                    print(f"%s%{mx+1}s%s  MOD  Size (KiB)"%(c.Back.GREEN,f"  ".join([i for i in pathlib.Path(path).absolute().__str__().replace("\\","/").split("/")]),f" {c.Back.RESET}{c.Fore.GREEN}{c.Fore.RESET}"))
                    for i in fileList:
                        pathnlx=pathlib.Path(path+"/"+i)
                        if pathnlx.is_dir():
                            print(
                                f"{c.Back.CYAN}%{mx}s%s {c.Fore.MAGENTA}{c.Fore.RESET}{c.Back.MAGENTA}DIR{c.Back.RESET}{c.Fore.MAGENTA}{c.Fore.RESET} %s"
                                %
                                (f"  ".join([pathlib.Path(path+"/"+i).relative_to(pathlib.Path(path)).__str__()]),f"/ {c.Back.RESET}{c.Fore.CYAN}{c.Fore.RESET}",
                                f"{'{:,}'.format(numerize.round_num(Decimal(get_folder_size(pathnlx.__str__())/1024),2))}"
                                )
                            )
                        else:
                            print(
                                f"{c.Back.YELLOW}%{mx+1}s%s %s %s"
                                %
                                (f"  ".join([pathlib.Path(path+"/"+i).relative_to(pathlib.Path(path)).__str__()]),f" {c.Back.RESET}{c.Fore.YELLOW}{c.Fore.RESET}",
                                f"{c.Fore.YELLOW}{c.Fore.RESET}{c.Back.YELLOW}ALL{c.Back.RESET}{c.Fore.YELLOW}{c.Fore.RESET}" 
                                    if os.access(pathnlx.__str__(),os.R_OK|os.W_OK|os.F_OK) 
                                    else 
                                    f"{c.Fore.RED}{c.Fore.RESET}{c.Back.RED}EXC{c.Back.RESET}{c.Fore.RED}{c.Fore.RESET}"
                                    if os.access(pathnlx.__str__(),os.W_OK) else
                                    f"{c.Fore.RED}{c.Fore.RESET}{c.Back.RED}ROF{c.Back.RESET}{c.Fore.RED}{c.Fore.RESET}"
                                    if os.access(pathnlx.__str__(),os.R_OK) else
                                    "     ",
                                f"{'{:,}'.format(numerize.round_num(Decimal(os.path.getsize(pathnlx.__str__())/1024),2))}"
                                )
                            )
                elif os.path.exists(r) and r.endswith(".tsh"):
                    self.execute(open(r).read())
                else:
                    if is_valid_python_code(r) and "--NoPy" and r.split()[0] not in self.allcommands:
                        try:
                            exec(add_global_to_variables(r))
                            continue
                        except:
                            pass
                    os.system(f"cmd.exe /c "+r.replace("/","\\"))
        self.namespace.update()
    def is_valid_expression(self,s):
        # Regular expression to match a valid Python expression
        pattern = r"^[\^+-/*%=<>!()\[\]{},.0-9\s]*$"
        if re.match(pattern, s):
            return True
        return False