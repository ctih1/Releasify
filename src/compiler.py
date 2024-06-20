import os
from tqdm import tqdm
def compile(commands:list)->list:
    files:list=[]
    for step in tqdm(commands):
        tqdm.write(f"\nRunning command for file {step['name']}\n\n\n\n\n\n")
        os.system(step["command"])
        files.append({"file":step["file"],"name":step["name"]})
    return files
    