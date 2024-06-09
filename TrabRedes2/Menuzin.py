import threading
from datetime import date, time
import time
from matplotlib import pyplot as plt

import ConsumoDados as funcs
sair = True

def menuOpcoes():
    print("===MENU===")
    print("Pesquisar cotação atual [0]\nPesquisar Cotação de um período [1]\nDeterminar moeda para vigiar [2]\n"
          "Sair [3]")
    opcao = int(input())
    return opcao

def gerarData():
    print("Ano: ")
    ano = int(input())
    print("Mes: ")
    mes = int(input())
    print("Dia: ")
    dia = int(input())
    return date(year=ano,month=mes,day=dia)

def exibirGraficos(lista_cotacoes_periodo):
    eixoY = [item["bid"] for item in lista_cotacoes_periodo]
    eixoX = [item["data"] for item in lista_cotacoes_periodo]

    plt.plot(eixoX, eixoY)
    eixoX_to_show = [eixoX[0], eixoX[len(eixoX) // 2], eixoX[-1]]
    plt.xticks(eixoX_to_show)
    plt.xlabel('Período')
    plt.ylabel('Valores')
    plt.title('Linha do tempo do valor de compra da moeda')

    # Mostrar o gráfico
    plt.show()

def monitorarTaxaCambio(moeda, moeda_base, limiar_superior, limiar_inferior):
    while sair:
        resposta = funcs.buscarInfoCambio([moeda], moeda_base)
        cotacao_atual = float(resposta[moeda]["bid"])  # Supondo que "bid" seja o campo da cotação de compra

        if cotacao_atual > limiar_superior:
            print("\n=========================")
            print(f"Alerta: Cotação do {moeda} está acima do limiar superior de {limiar_superior}: {cotacao_atual}")
            print("=========================\n")
        elif cotacao_atual < limiar_inferior:
            print("\n=========================")
            print(f"Alerta: Cotação do {moeda} está abaixo do limiar inferior de {limiar_inferior}: {cotacao_atual}")
            print("=========================\n")
        time.sleep(60)  # Esperar 60 segundos antes de verificar novamente

while(sair):
    listaMoedas = []
    opcao = menuOpcoes()
    if (opcao == 0):
        print("Qual moeda? [USD] || [EUR]")
        moeda = [input()]
        moeda_base = 'BRL'
        resposta = funcs.buscarInfoCambio(moeda,moeda_base)
        string_resposta = funcs.gerarMensagemCotacao(resposta[moeda[0]])
        print(string_resposta)

    if (opcao == 1):
        print("\nData inicial:")
        data_inicio = gerarData()
        print("\nData final:")
        data_fim = gerarData()
        print("Qual moeda? [USD] || [EUR]")
        moeda = input()
        moeda_base = 'BRL'
        lista_cotacoes_periodo = funcs.gerarListaCotacoesPeriodo(data_inicio, data_fim, moeda, moeda_base)
        exibirGraficos(lista_cotacoes_periodo)

    elif opcao == 2:
        print("Qual moeda deseja vigiar? [USD] || [EUR]")
        moeda = input()
        moeda_base = 'BRL'
        print("Defina o limiar superior: ")
        limiar_superior = float(input())
        print("Defina o limiar inferior: ")
        limiar_inferior = float(input())

        thread_monitoramento = threading.Thread(
            target=monitorarTaxaCambio,
            args=(moeda, moeda_base, limiar_superior, limiar_inferior)
        )
        thread_monitoramento.start()
        print(f"\nMonitorando {moeda}...\n")

    elif opcao == 3:
        sair = False




