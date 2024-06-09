import requests
import matplotlib.pyplot as plt
from datetime import datetime,timedelta, date
from pytz import timezone
url = "https://economia.awesomeapi.com.br/last/"
url_periodo = "https://economia.awesomeapi.com.br/json/daily/"

def getJsonCotacao(moedas,moeda_base):
    busca = []
    busca = [f"{item}-{moeda_base}" for item in moedas]
    string_busca = ','.join(busca)
    response = requests.get(f"{url}{string_busca}")
    json_response = response.json()
    return json_response

def gerarTableCotacao(moedas,moeda_base):

    tabela_cotacoes = {}
    content = getJsonCotacao(moedas,moeda_base)
    tabela_cotacoes = {item:content[item+moeda_base] for item in moedas}
    return tabela_cotacoes

def ajustarTimestamp(tabela):
    try:
        timestamp = float(tabela['timestamp'])
        dt = datetime.fromtimestamp(timestamp, tz=timezone("America/Sao_Paulo"))
        dt_formatada = dt.strftime("%d/%m/%Y")
        tabela['timestamp'] = dt_formatada
    except ValueError:
        print("não foi possível converter o valor do timestamp para um número")

    tabela['data'] = tabela['timestamp']
    del tabela['timestamp']
    return tabela

def ajustaTabela(tabela):
    del tabela['code']
    del tabela['codein']
    del tabela['create_date']
    tabela['pctChange'] += "%"
    tabela = ajustarTimestamp(tabela)
    return tabela

def gerarMensagemCotacao(tabela):
    mensagem = f"{tabela['name']}\nValor de compra = {tabela['bid']}\nValor de venda = {tabela['ask']}\nPorcentagem de variação = {tabela['pctChange']}"
    return mensagem

def getJsonCotacaoPeriodo(moeda,moeda_base,start_date,end_date):
#Trabalhar aqui
    busca = f"{moeda}-{moeda_base}"
    response = requests.get(f"{url_periodo}{busca}/?start_date={start_date}&end_date={end_date}")
    json_response = response.json()
    return json_response

def gerarListaDatas(data_inicio, data_fim):
    delta = data_fim - data_inicio
    lista_datas = []
    for i in range(delta.days + 1):
        day = data_inicio + timedelta(days=i)
        lista_datas.append(day)
    return  lista_datas

def ajustarTabelaDoPeriodo(json):

    for i, item in enumerate(json):
        if (i == 0):
            json[0] = ajustaTabela(json[0])
        else:
            json[i] = ajustarTimestamp(json[i])
    return json

def buscarInfoCambio(moedas,moeda_base):
    tabela = gerarTableCotacao(moedas,moeda_base)
    string_info = ''
    for moeda in moedas:
        ajustaTabela(tabela[moeda])
        string_info += f"{gerarMensagemCotacao(tabela[moeda])} \n\n"
    return string_info

#PROMPT

'''moedas = ['USD','EUR']
moeda_base = 'BRL'
resultado_busca = buscarInfoCambio(moedas,moeda_base)
print(resultado_busca)'''

########################
#Consulta por período
########################

start_date="20200201"
end_date="20200229"
moeda_base = 'BRL'

jsonPeriodo = getJsonCotacaoPeriodo("USD",moeda_base,start_date,end_date)
listaPeriodo = ajustarTabelaDoPeriodo(jsonPeriodo)
print(listaPeriodo)
