
class Times:
    def __init__(self, nome) -> None:
        self.nome = nome
        self.jogadores = []
    pass
    #SET
    def setNome(self,nome):
        self.nome = nome
    def setJogadores(self,jogadores):
        self.jogadores = jogadores
    #GET
    def getNome(self):
        return self.nome
    def getJogadores(self):
        return self.jogadores


#time1 = Times("nome", "jogadores")
#print(time1.nome)
#print(time1.jogadores)
#time1.setNome("Outro")
#print(time1.getNome())