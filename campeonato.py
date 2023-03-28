from rodada import *
from times import *
from partida import *
import random

class Campeonato:
    def __init__(self) -> None:
        self.times = []
        self.rodada = []
        self.tabela = []
        self.classificacao = []
    pass
    #SET
    def setTimes(self):
        x = 1
        while x==1: 
            qtdTimes = input("Digite a quantidade de times neste campeonato: ")
            if int(qtdTimes) % 2 != 0:
                print("Deve ter um número par de times.")
            else:
                x=0
        for y in range(int(qtdTimes)):
            nome = input("Nome do time: ")
            time = Times(nome)
            self.times.append(time)
        
    def listaTimesCadastrado(self):
        for x in self.times: 
            print (x.getNome())

    def setRodadas(self):
        qtdRodada = len(self.times)
        ultimo = len(self.times)-1
        for x in range(int(qtdRodada)):
            for y in range(int(len(self.times)/2)):
                partida = Partida(self.times[y],self.times[ultimo])
                self.rodada[x].append(partida)
                ultimo = ultimo - 1
            self.tabela[x].append(partida)
    
    def rodada(self):
        for x in self.rodadas:
            x.
    #GET
    def getTimes(self):
        return self.times
    def getRodadas(self):
        return self.rodadas

