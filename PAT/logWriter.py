from os import path

class LogWriter:
    #TODO: replace all csv writing to json writing
    #pass log as a list of a list of strings (every sub list is a single tick)
    @staticmethod
    def writeLevelLog(log,levelNum = 0,roundNum = 0):
        logFile = open(path.join(path.dirname(path.abspath(__file__)),f"logs/level{levelNum}round{roundNum}.csv"),"w+")
        
        for line in log:
            for entry in line:
                logFile.write(entry+",")
            logFile.write("\n")

    #questions passed in as a list of strings
    #answers passed in as a list of lists (multiple answers)
    @staticmethod
    def writeLevelQA(Q,A,levelNum = 0):
        logFile = open(path.join(path.dirname(path.abspath(__file__)),f"logs/level{levelNum}Answers.csv"),"w+")
        
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
        
    