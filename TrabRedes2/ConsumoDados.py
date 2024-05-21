import requests
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import timezone
url = "https://economia.awesomeapi.com.br/last/"
url_periodo = "https://economia.awesomeapi.com.br/"

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

def ajustaTabela(tabela):
    del tabela['code']
    del tabela['codein']
    del tabela['name']
    del tabela['create_date']
    ajustarTimestamp(tabela)

def getJsonCotacaoPeriodo(moeda,moeda_base,start_date,end_date):

    busca = f"{moeda}-{moeda_base}"
    response = requests.get(f"{url_periodo}{busca}/5?start_date={start_date}&end_date={end_date}")
    json_response = response.json()
    return json_response

def ajustarTabelaDoPeriodo(json):
    #?????
    temp = ajustaTabela(json[0])
    print(temp)


moedas = ['USD','EUR']
moeda_base = 'BRL'

tabela = gerarTableCotacao(moedas,moeda_base)

for moeda in moedas:
    ajustaTabela(tabela[moeda])

########################
#Consulta por período
########################

start_date="20200201"
end_date="20200229"

jsonPeriodo = getJsonCotacaoPeriodo("USD",moeda_base,start_date,end_date)
listaPeriodo = ajustarTabelaDoPeriodo(jsonPeriodo)
