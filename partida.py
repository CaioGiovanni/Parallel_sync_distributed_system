#from times import *
#import times

class Partida:
    def __init__(self, time1, time2) -> None:
        self.time1 = time1 #Objeto time
        self.time2 = time2 #Objeto time
        self.golTime1 = 0
        self.golTime2 = 0
        self.relatorio = ""
    pass
    #SET
    def setTime1(self,time1):
        self.time1 = time1
    def setTime1(self,time2):
        self.time2 = time2
    def setGolTime1(self,golTime1):
        self.golTime1 = golTime1
    def setGolTime2(self,golTime2):
        self.golTime2 = golTime2
    def setGolTime2(self,relatorio):
        self.relatorio = relatorio
    #GET
    def getTime1(self):
        return self.time1
    def getTime1(self):
        return self.time2
    def getGolTime1(self):
        return self.golTime1
    def getGolTime2(self):
        return self.golTime2
    def getGolTime2(self):
        return self.relatorio
