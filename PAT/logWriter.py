from os import path
from toExe import EXE



class LogWriter:
    #TODO: replace all csv writing to json writing
    #pass log as a list of a list of strings (every sub list is a single tick)
    @staticmethod
    def writeLevelLog(log,levelNum = 0,roundNum = 0):
        file = EXE.resource_path(f"logs/level{levelNum}round{roundNum}.csv")
        logFile = open(file,"w+")
        
        for line in log:
            for entry in line:
                logFile.write(entry+",")
            logFile.write("\n")

        logFile.close()

    #questions passed in as a list of strings
    #answers passed in as a list of lists (multiple answers)
    @staticmethod
    def writeLevelQA(Q,A,levelNum = 0):
        file =  EXE.resource_path(f"logs/level{levelNum}Answers.csv")
        logFile = open(file,"w+")
        
        initLine = "Question,Answers\n"
        logFile.write(initLine)

        index = 0
        for q in Q:
            logFile.write(f"{q},")

            for a in A[index]:
                logFile.write(a)
            logFile.write("\n")
            index += 1


        logFile.close()
        
    