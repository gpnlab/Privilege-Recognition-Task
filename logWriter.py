import os
from os import path
from datetime import datetime
import json

class LogWriter:

    def __init__(self,presetName = "default",name = "NONAME", timeStamp = "NOTIME",seed = 0):
        """
        This function initializes the class with the presetName, name, timeStamp, and seed
        
        Args:
          presetName: The name of the preset. Defaults to default
          name: The name of the preset. Defaults to NONAME
          timeStamp: The time the preset was created. Defaults to NOTIME
          seed: The seed for the random number generator. Defaults to 0
        """
        self.name = name
        self.timeStamp = timeStamp
        self.seed = seed

    def getPath(self):
        """
        It returns the path of the directory where the Python executable is located
        
        Returns:
          The path to the directory containing the Python interpreter.
        """
        return os.path.dirname(os.sys.executable)
    
    def writeSeed(self):
        """
        It creates a folder with the name of the current time stamp, and then creates a file
        called seed.txt inside of that folder
        """
        url = path.join(self.getPath(),f"logs/{self.name}/{self.timeStamp}")
        if not path.exists(url):
            os.makedirs(url)
        
        newFile = open(url + "/seed.txt","w+")

        newFile.write(str(self.seed))

    #TODO: replace all csv writing to json writing
    #pass log as a list of a list of strings (every sub list is a single tick)
    def writeLog(self,log):
        """
        It takes a log object, converts it to a json string, and writes it to a file
        
        Args:
          log: the log object
        """
        url = path.join(self.getPath(),f"logs/{self.name}/{self.timeStamp}")
        print("log writing to: " + url)
        if not path.exists(url):
            os.makedirs(url)
        url += "/data.json"  
        #assumed that file will be created via qa write so we can append      
        logFile = open(url,"w+")
        
        parsed = json.dumps(log, indent = 5)
        logFile.write(parsed)
        logFile.close()

    # UNUSED
    def writeLevelLog(self,log,levelName,roundNum = 0):
        """
        It takes a log, a level name, and a round number, and writes it to a file
        
        Args:
          log: the log object
          levelName: The name of the level
          roundNum: the round number of the level. Defaults to 0
        """
        url = path.join(self.getPath(),f"logs/{self.name}/{self.timeStamp}")
        
        if not path.exists(url):
            os.makedirs(url)

        url += "/data.json"  
        #assumed that file will be created via qa write so we can append      
        logFile = open(url,"a")
        
        parsed = json.dumps(log, indent = 5)

        logFile.write(parsed)

        logFile.close()

    #questions passed in as a list of strings
    #answers passed in as a list of lists (multiple answers)
    # UNUSED
    def writeLevelQA(self,qDict):
        """
        It takes a dictionary of data, converts it to a JSON string, and writes it to a file
        
        Args:
          qDict: A dictionary of the questions and answers.
        """
        url = path.join(self.getPath(),f"logs/{self.name}/{self.timeStamp}")
        
        if not path.exists(url):
            os.makedirs(url)
        
        url += f"/data.json"

        logFile = open(url,"w+")

        parsed = json.dumps(qDict, indent = 5)
        logFile.write(parsed)

        logFile.close()
        
    