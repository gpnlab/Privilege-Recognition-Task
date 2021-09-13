from os import path
from toExe import EXE
import json
class ConfigReader:
    def parseToDict(filename):
        url = EXE.resource_path(f"config/{filename}")
        with open(url,"r+") as config:
            d = json.load(config)
        print(f"loaded config {filename}")

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
