from os import path

class ConfigReader:
    def parseToDict(filename):
        d = dict()
        config = open(path.join(path.dirname(__file__),f"config/{filename}"),"r+")
        
        print(f"loaded config {filename}")
        qList = []
        for line in config.readlines():

            #parse line by =
            i = line.find("=")

            key = line[:i].strip()
            val = line[i + 1 :]


            if key == "question":
                qList.append(val.strip())
            
            else: #its some num
                d[key] = float(val)

        
        d["question"] = qList
        
        config.close()
        return d
