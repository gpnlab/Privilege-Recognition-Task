from os import path

class LogWriter:

    #pass log as a list of a list of strings (every sub list is a single tick)
    @staticmethod
    def writeLevelLog(log,levelNum = 0,roundNum = 0):
        logFile = open(path.join(path.dirname(__file__),f"logs/level{levelNum}round{roundNum}.csv"),"w+")
        
        for line in log:
            for entry in line:
                logFile.write(entry+",")
            logFile.write("\n")
                


        logFile.close()
        
    