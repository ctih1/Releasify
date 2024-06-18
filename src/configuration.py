import json
class Configurator:
    def load(repo:str,self) -> dict:
        with open("../config.json","r") as f:
            data: dict=json.load(f)
        return data.get(repo,{})
