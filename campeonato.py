#from rodada import *
import random
import rodada
import times

class Campeonato:
    def __init__(self) -> None:
        self.times = []
        self.rodadas = []
        self.classificacao = []
    pass
    #SET
    def setTimes(self):
        x = 1
        while x==1: 
            qtdTimes = input("Digite a quantidade de times neste campeonato: ")
            if qtdTimes%2 != 0:
                print("Deve ter um número par de times.")
            else:
                x=0
        for y in qtdTimes:
            nome = input("Nome do time "+y+": ")
            time = times(nome)
            self.times.append(time)

    def setRodadas(self):
        qtdRodada = len(self.times) - 1

        for x in qtdRodada:
            for y in len(self.times)/2:
                w = 1
                repetido = []
                while w == 1:
                    a = random.randint(1,qtdRodada)
                    b = random.randint(1,qtdRodada)
                    if a!=b and (a in repetido) and (b in repetido):
                        partida = partida(self.times[a],self.times[b])
                        repetido.append(a)
                        repetido.append(b)
                        y=0
                self.rodadas[x].append(partida)
            
    #GET
    def getTimes(self):
        return self.times
    def getRodadas(self):
        return self.rodadas

