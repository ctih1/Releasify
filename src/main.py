from flask import Flask,request

app = Flask(__name__)
@app.route("/webhook",methods=["POST"])
def webhook():
	print(request.json)
	if(request.json.get("action")=="published"):
		print("new release")
	print("Recieved webhook")
	return "OK",200


app.run()
