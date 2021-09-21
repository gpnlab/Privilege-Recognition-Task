import os
from os import path
from datetime import datetime

class LogWriter:

    def __init__(self,presetName = "default",name = "NONAME", timeStamp = "NOTIME",seed = 0):
        self.presetName = presetName
        self.name = name
        self.timeStamp = timeStamp
        self.seed = seed

    def writeSeed(self):
        url = path.join(path.dirname(path.abspath(__file__)),f"logs/{self.name}/{self.presetName},{self.timeStamp}")
        if not path.exists(url):
            os.makedirs(url)
        
        newFile = open(url + "/seed.txt","w+")

        newFile.write(str(self.seed))

    #TODO: replace all csv writing to json writing
    #pass log as a list of a list of strings (every sub list is a single tick)

    def writeLevelLog(self,log,levelName,roundNum = 0):
        url = path.join(path.dirname(path.abspath(__file__)),f"logs/{self.name}/{self.presetName},{self.timeStamp}/data")
        
        if not path.exists(url):
            os.makedirs(url)

        url += f"/{levelName}-round{roundNum}.csv"
        
        logFile = open(url,"w+")
        
        for line in log:
            for entry in line:
                logFile.write(entry+",")
            logFile.write("\n")

        logFile.close()

    #questions passed in as a list of strings
    #answers passed in as a list of lists (multiple answers)

    def writeLevelQA(self,Q,A,levelName):
        url = path.join(path.dirname(path.abspath(__file__)),f"logs/{self.name}/{self.presetName},{self.timeStamp}/answers")
        
        if not path.exists(url):
            os.makedirs(url)
        
        url += f"/{levelName}-answers.json"

        logFile = open(url,"w+")
        
        initLine = '{\n'
        logFile.write(initLine)

        index = 0

        for q in Q:

            logFile.write(f'\t"Question{index}": {"{"}\n\t\t"name": "{q}",\n\t\t"answer": ')

            aIndex = 0 
            logFile.write("[")

            for a in A[index]:

                aIndex += 1
                if aIndex < len(A[index]):
                    logFile.write(f'"{a}",')
                else:
                    logFile.write(f'"{a}"]')
            

            index += 1

            if index < len(Q):
                logFile.write("\n\t},\n")
            else:
                logFile.write("\n\t}\n")



        logFile.write("}")

        logFile.close()
        
    