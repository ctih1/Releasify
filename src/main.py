from flask import Flask,request
import dotenv
import requests
import json
import os
from configuration import Configurator
import compiler

dotenv.load_dotenv("../.env")
gh_token:str=os.getenv("GH_AUTH_KEY")
app = Flask(__name__)
conf:Configurator =Configurator()

@app.route("/webhook",methods=["POST"])
def webhook():
	with open("response.json","w") as f: json.dump(request.json,f)
	if(request.json.get("action")=="published"): # if the release is published, not deleted or mdified
     
		id:int = int(request.json.get("release",{}).get("id",-1))
		repo_username:str = str(request.json.get("repository",{}).get("full_name",""))
		if(id==-1): return
		conf_data = conf.load(request.json.get("repository"))
		compiler.compile(
      		command=conf_data.get("command"),
			filename=conf_data.get("file")
      	)
		with open(conf_data.get("file"),"rb") as f:
			filedata=f.read()
		response=requests.post(
			f"https://uploads.github.com/repos/{repo_username}/releases/{str(id)}/assets?name={conf_data.get('file')}",
			data=filedata,
			headers={"Accept":"application/vnd.github+json",
				"Authorization": "Bearer "+gh_token,
				"X-GitHub-Api-Version":"2022-11-28",
				"Content-Type":"application/octet-stream"
			 })
		print(response.status)	
	print("Recieved webhook")
	return "OK",200
app.run()
