import os
from os import path
from datetime import datetime
import json

class LogWriter:

    def __init__(self,presetName = "default",name = "NONAME", timeStamp = "NOTIME",seed = 0):
        self.name = name
        self.timeStamp = timeStamp
        self.seed = seed

    def getPath(self):
        return os.path.dirname(os.sys.executable)
    def writeSeed(self):
        url = path.join(self.getPath(),f"logs/{self.name}/{self.timeStamp}")
        if not path.exists(url):
            os.makedirs(url)
        
        newFile = open(url + "/seed.txt","w+")

        newFile.write(str(self.seed))

    #TODO: replace all csv writing to json writing
    #pass log as a list of a list of strings (every sub list is a single tick)
    def writeLog(self,log):
        url = path.join(self.getPath(),f"logs/{self.name}/{self.timeStamp}")
        print("writing to: " + url)
        if not path.exists(url):
            os.makedirs(url)
        url += "/data.json"  
        #assumed that file will be created via qa write so we can append      
        logFile = open(url,"w")
        
        parsed = json.dumps(log, indent = 5)
        logFile.write(parsed)
        logFile.close()

    # UNUSED
    def writeLevelLog(self,log,levelName,roundNum = 0):
        url = path.join(self.getPath(),f"logs/{self.name}/{self.timeStamp}")
        
        if not path.exists(url):
            os.makedirs(url)

        url += "/data.json"  
        #assumed that file will be created via qa write so we can append      
        logFile = open(url,"a")
        
        parsed = json.dumps(log, indent = 5)

        #print(parsed)
        logFile.write(parsed)

        # for line in log:
        #     for entry in line:
        #         logFile.write(entry+",")
        #     logFile.write("\n")

        logFile.close()

    #questions passed in as a list of strings
    #answers passed in as a list of lists (multiple answers)
    # UNUSED
    def writeLevelQA(self,qDict):
        url = path.join(self.getPath(),f"logs/{self.name}/{self.timeStamp}")
        
        if not path.exists(url):
            os.makedirs(url)
        
        url += f"/data.json"

        logFile = open(url,"w+")

        parsed = json.dumps(qDict, indent = 5)
        print(parsed)
        logFile.write(parsed)
        # initLine = '{\n'
        # logFile.write(initLine)

        # index = 0

        # for q in Q:

        #     logFile.write(f'\t"Question{index}": {"{"}\n\t\t"name": "{q}",\n\t\t"answer": ')

        #     aIndex = 0 
        #     logFile.write("[")

        #     for a in A[index]:

        #         aIndex += 1
        #         if aIndex < len(A[index]):
        #             logFile.write(f'"{a}",')
        #         else:
        #             logFile.write(f'"{a}"]')
            

        #     index += 1

        #     if index < len(Q):
        #         logFile.write("\n\t},\n")
        #     else:
        #         logFile.write("\n\t}\n")



        # logFile.write("}")

        logFile.close()
        
    