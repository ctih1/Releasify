from flask import Flask,request
import dotenv
import requests
import json
import os
from tqdm import tqdm
from configuration import Configurator as conf
import compiler

dotenv.load_dotenv("../.env")
gh_token:str=os.getenv("GH_AUTH_KEY")
app = Flask(__name__)

@app.route("/webhook",methods=["POST"])
def webhook():
    tqdm.write("Webhook recieved!")
    with open("response.json","w") as f: json.dump(request.json,f)
    if(request.json.get("action")=="published"): # if the release is published, not deleted or mdified
        id:int = int(request.json.get("release",{}).get("id",-1))
        repo_username:str = str(request.json.get("repository",{}).get("full_name",""))
        if(id==-1): 
            tqdm.write("Release ID is not valid, aborting")
            return
        repo_name = request.json.get("repository",{}).get("name")
        conf_data = conf.load(repo_name)
        files = compiler.compile(
            commands=conf_data.get("steps"),
        )
        for file in files:
            tqdm.write(f"Loading {file['file']}...")
            with open(file["file"],"rb") as f:
                filedata=f.read()
            tqdm.write(f"Uploading file {file['name']} to GitHub")
            response=requests.post(
                f"https://uploads.github.com/repos/{repo_username}/releases/{str(id)}/assets?name={file['name']}",
                data=filedata,
                headers={
                    "User-Agent":"request",
                    "Accept":"application/vnd.github+json",
                    "Authorization": "Bearer "+gh_token,
                    "X-GitHub-Api-Version":"2022-11-28",
                    "Content-Type":"application/octet-stream"
                })
            if(response.status_code!=200):
                tqdm.write(f"Upload failed: {response.json()}")
            else:
                tqdm.write(f"Succesfully uploaded {file['name']}")
    return "OK",200
app.run()
