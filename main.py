from re import A
import time
import random

#REALIZA PARTIDA
def eventosPartidas(time1,time2):
    eventoLista = [
        "Gol do "+time1,
        "Gol do "+time2,
        "Jogo rolando"
    ]
    evento = random.randint(1, 10)
    if evento == 2 or evento == 1 or evento == 3:
        return eventoLista[0],time1
    elif evento == 5 or evento == 4 or evento == 6:
        return eventoLista[1],time2
    else:
        return eventoLista[2],"-"

def jogo(partida):
    time1 = partida[0]
    time2 = partida[1]
    golTime_1 = 0
    golTime_2 = 0
    statusPartida = 0

    tempo_inicial = time.time()
    tempo_atual = time.time()
    tempoAtualizacao = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

    print("----PARTIDA----")
    print(time1[0] + " X " + time2[0])
    print("---------------")
    while tempo_atual - tempo_inicial < 10:

        if int(tempo_atual - tempo_inicial) in tempoAtualizacao:
            evento, equipe = eventosPartidas(time1[0],time2[0])
            if equipe == time1[0]:
                golTime_1 = golTime_1 + 1
            elif equipe == time2[0]:
                golTime_2 = golTime_2 + 1
            print(evento)
            tempoAtualizacao.pop(0)

        tempo_atual = time.time()

    print("FIM DA PARTIDA")
    print("RESULTADO")
    print(time1[0] + " " + str(golTime_1) + " X " + str(golTime_2) + " " + time2[0])
    print(" ")

    if golTime_1 > golTime_2:
        statusPartida = 1
    elif golTime_2 > golTime_1:
        statusPartida = 2

    return golTime_1, golTime_2, statusPartida

def realizaPartida(partida,time1,time2,classificacao,historicoPartida):
    golTime_1, golTime_2, statusPartida = jogo(partida)
    time1[2] = time1[2]+golTime_1
    time2[2] = time2[2]+golTime_2
    time1, time2 = pontuaTime(time1, time2, statusPartida)
    partidaInfo = [time1[0],golTime_1,time2[0],golTime_2]
    historicoPartida.append(partidaInfo)
    classificacao = exibeClassificacao(classificacao)
    return time1, time2,classificacao

#PONTUA TIME
def pontuaTime(Time1,Time2,status):
    if status == 1:
        Time1[1] = Time1[1] + 3
    elif status == 2:
        Time2[1] = Time2[1] + 3
    else:
        Time1[1] = Time1[1] + 1
        Time2[1] = Time2[1] + 1
    return Time1, Time2

#CLASSIFICACAO
def exibeClassificacao (classificacao):
    classificacao = sorted(classificacao, key=lambda x: x[1], reverse=True)
    print("---------------------------------")
    print("CLASSIFICACAO")
    print("---------------------------------")
    i=0
    for x in classificacao:
        i = i + 1
        print(str(i) + "-" + x[0] + " pontos: " + str(x[1]) + " qtd de gols: " + str(x[2]))
    print("---------------------------------")
    return classificacao

def exibeHistorico (historicoPartida):
    i = 1
    a = 1
    print("----PLACARES DAS RODADAS----")
    for x in historicoPartida:
        if i==1 or i == 4 or i == 7 or i == 10 or i==13 or i==16:
            a = a+1
            print("RODADA " + str(a))
        print(x[0] + " " + str(x[1]) + "  X  " + str(x[3]) + " " + str(x[2]))
        i = i+1


def main():
    print("TesteGit")
    #-------------------------------------
    #TIMES [Nome, pontos, qtdGols]
    timeA = ["TimeA",0,0]
    timeB = ["TimeB",0,0]
    timeC = ["TimeC",0,0]
    timeD = ["TimeD",0,0]
    timeE = ["TimeE",0,0]
    timeF = ["TimeF",0,0]

    classificacao = [timeA,timeB,timeC,timeD,timeE,timeF]
    historicoPartida = []
    #-------------------------------------
    #RODADA1
    print("--------------------RODADA 1--------------------")
    Partida1A= [timeA, timeB]
    timeA,timeB,classificacao = realizaPartida(Partida1A,timeA,timeB,classificacao,historicoPartida) #Maquina1

    Partida1B= [timeC, timeD]
    timeC,timeD,classificacao = realizaPartida(Partida1B,timeC,timeD,classificacao,historicoPartida) #Maquina2

    Partida1C= [timeE, timeF]
    timeE,timeF,classificacao = realizaPartida(Partida1C,timeE,timeF,classificacao,historicoPartida) #Maquina3
    exibeHistorico (historicoPartida)
    #-------------------------------------
    print("--------------------RODADA 2--------------------")
    Partida2A = [timeA, timeC]
    timeA,timeC,classificacao = realizaPartida(Partida2A,timeA,timeC,classificacao,historicoPartida) #Maquina1

    Partida2B = [timeD, timeE]
    timeD,timeE,classificacao = realizaPartida(Partida2B,timeD,timeE,classificacao,historicoPartida) #Maquina2
    
    Partida2C = [timeF, timeB]
    timeF,timeB,classificacao = realizaPartida(Partida2C,timeF,timeB,classificacao,historicoPartida) #Maquina2

    exibeHistorico (historicoPartida)
    #-------------------------------------
    print("--------------------RODADA 3--------------------")
    Partida3A= [timeA, timeD]
    timeA,timeD,classificacao = realizaPartida(Partida3A,timeA,timeD,classificacao,historicoPartida) #Maquina1

    Partida3B= [timeE, timeB]
    timeE,timeB,classificacao = realizaPartida(Partida3B,timeE,timeB,classificacao,historicoPartida) #Maquina2

    Partida3C= [timeC, timeF]
    timeC,timeF,classificacao = realizaPartida(Partida3C,timeC,timeF,classificacao,historicoPartida) #Maquina3

    exibeHistorico (historicoPartida)
    #-------------------------------------
    print("--------------------RODADA 4--------------------")  
    Partida4A= [timeA, timeE]
    timeA,timeE,classificacao = realizaPartida(Partida4A,timeA,timeE,classificacao,historicoPartida) #Maquina1

    Partida4B= [timeB, timeC]
    timeB,timeC,classificacao = realizaPartida(Partida4B,timeB,timeC,classificacao,historicoPartida) #Maquina2

    Partida4C= [timeD, timeF]
    timeD,timeF,classificacao = realizaPartida(Partida4C,timeD,timeF,classificacao,historicoPartida) #Maquina3

    exibeHistorico (historicoPartida)
    #-------------------------------------
    print("--------------------RODADA 5--------------------")
    Partida5A= [timeA, timeF]
    timeA,timeF,classificacao = realizaPartida(Partida5A,timeA,timeF,classificacao,historicoPartida) #Maquina1

    Partida5B= [timeB, timeD]
    timeB,timeD,classificacao = realizaPartida(Partida5B,timeB,timeD,classificacao,historicoPartida) #Maquina2

    Partida5C= [timeC, timeE]
    timeC,timeE,classificacao = realizaPartida(Partida5C,timeC,timeE,classificacao,historicoPartida) #Maquina3
    
    exibeHistorico (historicoPartida)
    #-------------------------------------

    print(classificacao[0][0] + " É o grande campeao")
    print(classificacao[1][0] + " É o vice campeao")
    print(classificacao[5][0] + " É o lanterna")
    #PARTIDAS
    return 0

if __name__ == "__main__":
    main()