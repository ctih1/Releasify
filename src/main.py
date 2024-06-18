from flask import Flask,request
import dotenv
import requests
import json
import os
from configuration import Configurator as conf
import compiler

dotenv.load_dotenv("../.env")
gh_token:str=os.getenv("GH_AUTH_KEY")
app = Flask(__name__)


@app.route("/webhook",methods=["POST"])
def webhook():
	with open("response.json","w") as f: json.dump(request.json,f)
	if(request.json.get("action")=="published"): # if the release is published, not deleted or mdified
		print("Correct action")
		id:int = int(request.json.get("release",{}).get("id",-1))
		repo_username:str = str(request.json.get("repository",{}).get("full_name",""))
		if(id==-1): return
		repo_name = request.json.get("repository",{}).get("name")
		print(repo_name)
		conf_data = conf.load(repo_name)
		print(conf_data)
		files = compiler.compile(
			commands=conf_data.get("steps"),
		)
		print(f"files: {files}")
		for file in files:
			print(file)
			with open(file["file"],"rb") as f:
				filedata=f.read()

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
			print(f"recieved: {response.json()}")
	print("Recieved webhook")
	return "OK",200
app.run()
