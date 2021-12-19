"""
Created by: Guilherme De Assis, 10/11/2021

The main objetive is monitor TESLA action, you decide the percent of volatily from the market!
Test change stock name and company name, have a good time!
At API keys, account_sid of twilio (API for send messages for your phone) and tokens are confidencial informations,
so it was created enviroments variables, create yours enviroments variables.


O principal objetivo é monitorar as ações da TESLA, você decide a porcentagem da volatilidade do mercado!
Teste mudar o stock name (nome da ação) e o company name (nome da companhia), Divirta-se!
As chaves de API, o SID da sua conta do twilio (API para enviar mensagens para o seu telefone) e tokens são informações confidencias,
então foram criados variaveis de ambiente, crie sua variaveis de ambiente.

"""

import requests
import html
import os
from twilio.rest import Client
# ------------------------------------------------------------------------------------ #
# Nomes da ação e companhia / Stock name and company name
COMPANY_NAME = "Tesla Inc"
STOCK_NAME = "TSLA"

# ------------------------------------------------------------------------------------ #
# https://newsapi.org/ -> make your register and obtain your api key // faça seu cadastro e obtenha sua chave de API
NEWS_API_KEY = os.enviroment["NEWS_API_KEY"]

# ------------------------------------------------------------------------------------ #
# https://www.alphavantage.co/ -> make your register and obtain your api key // faça seu cadastro e obtenha sua chave de API
STOCK_KEY = os.enviroment["STOCK_KEY"]

# ------------------------------------------------------------------------------------ #
# https://www.twilio.com/pt-br/ -> make your register and obtain your account SID, TOKEN and Phone number
# Crie sua conta para obter o SID da conta, o token e o numero de telefone.
ACCOUNT_SID = os.enviroment["ACCOUNT_SID"]
AUTH_TOKEN = os.enviroment["AUTH_TOKEN"]
NUMBER = os.enviroment["NUMBER_TWIlIo"]
MY_NUMBER = "ENTER YOUR NUMBER"
PERCENT = 0  # Define the percentage for the program send a mesage for you 

# ------------------------------------------------------------------------------------ #
# Parameters for Stock Api // Paramêtros para o Stock Api
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_KEY
}

# ------------------------------------------------------------------------------------ #
# Parameters for news Api, The news API provides news on certains subjects // Parametros
# para o News API, O news api fornece noticias de determinados assuntos
news_parameters = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY
}
# ------------------------------------------------------------------------------------ #
# --------------------------------- END POINTS --------------------------------------- #
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"

# ------------------------------------------------------------------------------------ #
# ----------------------------------- RESPONSES -------------------------------------- #
stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()

# ------------------------------------------------------------------------------------ #
# ------------------------------ DATA PROCESSING ------------------------------------- #
daily_stock_data = stock_data['Time Series (Daily)']
new_daily_list = [item for (key, item) in daily_stock_data.items()]
yesterday_data = new_daily_list[0]
yesterday_close_price = float(yesterday_data["4. close"])
day_before_yesterday_data = new_daily_list[1]
before_yesterday_close_price = float(day_before_yesterday_data["4. close"])
difference_price = yesterday_close_price - before_yesterday_close_price

# ------------------------------------------------------------------------------------ #
# An emoji it's kind be a cool rs ! // Um emoji ate que e legal !
up_down = None
if difference_price > 0:
    up_down = "🔼"
else:
    up_down = "🔽"

# ------------------------------------------------------------------------------------ #
# Calculated and round de difference percent // Calculando e arredondando a diferença de
# Porcentagem 
difference_percent = round((difference_price / yesterday_close_price) * 100)

# ------------------------------------------------------------------------------------ #
# ------------------------------- SEND A MESSAGE ! ----------------------------------- #
if abs(difference_percent) > PERCENT:
    response = requests.get(NEWS_API_ENDPOINT, params=news_parameters)
    response.raise_for_status()
    news_data = response.json()
    articles_data = news_data["articles"][:3]
    three_titles = [
        f"{STOCK_NAME}: {up_down}{abs(difference_percent)}%  \n Headline: {articles['title']} \nBrief: {articles['description']}" for articles in articles_data
    ]
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for message in three_titles:
        message = client.messages\
            .create(
                body= message,
                from_= NUMBER,
                to="DESTINATARY"
            )
