import os
from pathlib import Path
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
    
    def get_path(self) -> Path:
        """Generate the directory for writing log-related files."""
        path = Path.cwd() / "logs" / self.name / self.timeStamp
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    def writeSeed(self):
        """
        It creates a folder with the name of the current time stamp, and then creates a file
        called seed.txt inside of that folder
        """
        path = self.get_path() / "seed.txt"
        with open(os.fspath(path), "w+") as seedfile:
            seedfile.write(str(self.seed))

    #TODO: replace all csv writing to json writing
    #pass log as a list of a list of strings (every sub list is a single tick)
    def writeLog(self,log: dict):
        """
        It takes a log object, converts it to a json string, and writes it to a file
        
        Args:
          log: the log object
        """
        path = self.get_path() / "data.json"
        print(f"log writing to: {os.fspath(path)}")
        with open(os.fspath(path), "w+") as logfile:
            parsed = json.dumps(log, indent=5)
            logfile.write(parsed)      

    # UNUSED
    def writeLevelLog(self,log,levelName,roundNum = 0):
        """
        It takes a log, a level name, and a round number, and writes it to a file
        
        Args:
          log: the log object
          levelName: The name of the level
          roundNum: the round number of the level. Defaults to 0
        """
        path = self.get_path() / "data.json"
        with open(os.fspath(path), "a") as logfile:
            parsed = json.dumps(qDict, indent=5)
            logfile.write(parsed)      

    #questions passed in as a list of strings
    #answers passed in as a list of lists (multiple answers)
    # UNUSED
    def writeLevelQA(self,qDict):
        """
        It takes a dictionary of data, converts it to a JSON string, and writes it to a file
        
        Args:
          qDict: A dictionary of the questions and answers.
        """
        path = self.get_path() / "data.json"
        with open(os.fspath(path), "w+") as logfile:
            parsed = json.dumps(qDict, indent=5)
            logfile.write(parsed)      
    