import requests

url = "https://economia.awesomeapi.com.br/last/"

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

moedas = ['USD','EUR']
moeda_base = 'BRL'

tabela = gerarTableCotacao(moedas,moeda_base)
