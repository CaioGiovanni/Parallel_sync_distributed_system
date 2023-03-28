from campeonato import *
#import campeonato

def main():
    campeonato = Campeonato()
    #Cadastra Times
    campeonato.setTimes()
    #campeonato.listaTimesCadastrado()
    #Prepara Rodadas
    campeonato.setRodadas()
    #campeonato.getRodadas()
    return 0

if __name__ == '__main__':
    main()