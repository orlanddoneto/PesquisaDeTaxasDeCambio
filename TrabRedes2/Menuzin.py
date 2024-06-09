import ConsumoDados as funcs
sair = True

def menuOpcoes():
    print("Pesquisar cotação atual [0]\nPesquisar Cotação de um periodo [1]\nDeterminar moeda para vigiar [2] ")
    opcao = int(input())
    return opcao

while(sair):
    listaMoedas = []
    opcao = menuOpcoes()
    if (opcao == 0):
        print("Qual moeda? [USD] || [EUR]")
        moeda = [input()]
        moeda_base = 'BRL'
        resposta = funcs.buscarInfoCambio(moeda,moeda_base)
        print(resposta)
