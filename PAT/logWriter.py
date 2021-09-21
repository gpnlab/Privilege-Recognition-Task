import os
from os import path
from datetime import datetime

class LogWriter:

    def __init__(self,presetName = "default",name = "NONAME", timeStamp = "NOTIME"):
        self.presetName = presetName
        self.name = name
        self.timeStamp = timeStamp
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

    #questions passed in as a list of strings
    #answers passed in as a list of lists (multiple answers)

    def writeLevelQA(self,Q,A,levelName):
        url = path.join(path.dirname(path.abspath(__file__)),f"logs/{self.name}/{self.presetName},{self.timeStamp}/answers")
        
        if not path.exists(url):
            os.makedirs(url)
        
        url += f"/{levelName}-answers.csv"

        logFile = open(url,"w+")
        
        initLine = "Question,Answers\n"
        logFile.write(initLine)

        index = 0
        print(Q)
        print(A)
        for q in Q:
            logFile.write(f"{q},")

            for a in A[index]:
                logFile.write(a)
            logFile.write("\n")
            index += 1


        logFile.close()
        
    