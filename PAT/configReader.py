from os import path
from exe import EXE
import json
from exe import EXE
class ConfigReader:

    #requires a json formated as in the default directory
    def parseToDict(filename,dirName = "default"):

        asset_url = EXE.resource_path(f"configs/{dirName}/{filename}.json")

        with open(asset_url,"r+") as config:
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
