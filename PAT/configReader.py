from os import path

class ConfigReader:
    def parseToDict(filename):
        d = dict()
        config = open(path.join(path.dirname(__file__),f"config/{filename}"),"r+")
        
        print(f"loaded config {filename}")
        for line in config.readlines():

            #parse line by =
            i = line.find("=")
            d[line[:i].strip()] = float(line[i + 1 :])
        
        config.close()
        return d
