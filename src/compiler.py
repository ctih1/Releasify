import os

def compile(commands:list)->list:
    files:list=[]
    for step in commands:
        print(step)
        os.system(step["command"])
        files.append({"file":step["file"],"name":step["name"]})
    return files
    

        