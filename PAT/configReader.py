from os import path
import json
class ConfigReader:
    def parseToDict(filename):
        with open(path.join(path.dirname(__file__),f"config/{filename}"),"r+") as config:
            d = json.load(config)
        print(f"loaded config {filename}")

        return d
