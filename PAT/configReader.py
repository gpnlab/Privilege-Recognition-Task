from os import path
from toExe import EXE
import json
from exe import EXE
class ConfigReader:
<<<<<<< HEAD

    #requires a json formated as in the default directory
    def parseToDict(filename,dirName = "default"):

        asset_url = EXE.resource_path(f"configs/{dirName}/{filename}.json")

        with open(asset_url,"r+") as config:
=======
    def parseToDict(filename):
        url = EXE.resource_path(f"config/{filename}")
        with open(url,"r+") as config:
>>>>>>> main
            d = json.load(config)
        print(f"loaded config {filename}")

        config.close()
        
        return d

    @staticmethod
    def returnQuestionText(self):
        retList = []
        for q in self.config["questions"]:
            retList.append(q["question"])
        return retList
    
    @staticmethod
    def returnQuestionText(self):
        retList = []
        for q in self.config["questions"]:
            retList.append(q["question"])
        return retList
