from os import path
import json
class ConfigReader:
    def parseToDict(filename):
        with open(path.join(path.dirname(__file__),f"config/{filename}"),"r+") as config:
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
