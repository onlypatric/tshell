import re

def FindSettings(string:str):
    obj:"dict[str,bool|str]"={};
    for i in re.findall("[\-\-|\-]+[A-Za-z0-9_-|=|\"]*",string):
        if "=" in i:
            splitted=i.split("=")
            obj[splitted[0].replace("-","")]="".join(re.findall("[^\"]",str(splitted[1])))
        else:
            obj[i.replace("-","")]=not obj.get(i.replace("--",""),False)
    return obj

def FindParams(string:str):
    obj:"list[str|object]"=[i for i in string.split() if re.match("^[^-]+",i)]
    while("" in obj):
        obj.remove('')
    return obj

if __name__=="__main__":
    params="file.py --hello main2.py object=\"23\" -w -world=320 --object=\"32bit\" main.py main-py.py main3.py"
    print(FindSettings(params))
    print(FindParams(params))