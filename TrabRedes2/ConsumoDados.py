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
        dt_formatada = dt.strftime("%Y%m%d")
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
    start_date = start_date.strftime("%Y%m%d")
    end_date = end_date.strftime("%Y%m%d")
    busca = f"{moeda}-{moeda_base}"
    response = requests.get(f"{url_periodo}{busca}/?start_date={start_date}&end_date={end_date}")
    json_response = response.json()
    return json_response[0]

def gerarListaDatas(data_inicio, data_fim):
    delta = data_fim - data_inicio
    lista_datas = []
    for i in range(delta.days + 1):
        day = data_inicio + timedelta(days=i)
        lista_datas.append(day)
    return lista_datas

def gerarListaCotacoesPeriodo(data_inicio,data_fim,moeda,moeda_base):
    lista_datas = gerarListaDatas(data_inicio,data_fim)
    lista_cotacoes_periodo = []
    for data in lista_datas:
        data_anterior = data - timedelta(days=3)
        tabela = getJsonCotacaoPeriodo(moeda,moeda_base,data_anterior,data)
        tabela = ajustaTabela(tabela)
        lista_cotacoes_periodo.append(tabela)

    return lista_cotacoes_periodo

def buscarInfoCambio(moedas,moeda_base):
    tabela = gerarTableCotacao(moedas,moeda_base)
    #string_info = ''
    for moeda in moedas:
        ajustaTabela(tabela[moeda])
        #string_info += f"{gerarMensagemCotacao(tabela[moeda])} \n\n"
    #return string_info
    return tabela

#PROMPT BUSCA COTAÇÃO DO DIA

'''moedas = ['USD','EUR']
moeda_base = 'BRL'
resultado_busca = buscarInfoCambio(moedas,moeda_base)
print(resultado_busca)'''

########################
#Consulta por período
########################


start_date= date(year=2020,month=2,day=1)
end_date = date(year=2020,month=2,day=29)
moeda_base = 'BRL'
moeda = 'USD'

lista_cotacoes_periodo = gerarListaCotacoesPeriodo(start_date,end_date,moeda,moeda_base)

#Gerar Gráficos
eixoY = [item["bid"] for item in lista_cotacoes_periodo]
eixoX = [item["data"] for item in lista_cotacoes_periodo]

plt.plot(eixoX,eixoY)
eixoX_to_show = [eixoX[0], eixoX[len(eixoX)//2], eixoX[-1]]
plt.xticks(eixoX_to_show)
plt.xlabel('Período')
plt.ylabel('Valores')
plt.title('Linha do tempo do valor de compra da moeda')

# Mostrar o gráfico
plt.show()

