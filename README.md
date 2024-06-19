# Releasify 
A simple webhook utility that creates a binary for your application when a new release is made

# Installation
```
git clone https://github.com/ctih1/Releasify
cd Releasify
pip install -r requirements.txt
*Configure JSON*
cd src
python main.py
```

# Configuration
First you need to grab yourself a [GitHub Personal access token](https://github.com/settings/tokens). Create a file called `.env` in the same directory where your `config.json` is, and write the following into the file: `GH_AUTH_KEY=""`, your key being inside the ""

Here's a small tutorial on how you should configure your `config.json`. 
```
{
    "Repo name": {
        "steps": [
            {
                "name":"File name shown on GitHub",
                "file":"The file location where your file will be found",
                "command": "The command that is run when the webhook is triggered"
            }
        ]
    }
}
```
Here's an example:
```
{
    "Releasify": {
        "steps": [
            {
                "name":"releasify-windows.exe",
                "file":"/home/ctih1/releasify/build/releasify-windows.exe",
                "command":"touch /home/ctih1/releasify/build/releasify-windows.exe"
            }
        ]
    }
}
```