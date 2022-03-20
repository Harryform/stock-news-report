import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "V32C0EPJV5S0YOSR"   # alpha advantage key
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "0003aa45b6c04c5c8a67c137727a15d7"
TWILIO_SID = "ACbea4ffd4267f5af210bf02f4be2c4f0e"
AUTH_TOKEN = "3203f2eda57a2fb25dc9c2bd3dc39a82"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']
day_before_data = data_list[1]
day_before_closing_price = day_before_data['4. close']

difference = float(yesterday_closing_price) - float(day_before_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)


if abs(diff_percent) > .5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()['articles']
    three_articles = articles[:3]

    message = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}, \nBrief: {article['description']}" for article in three_articles]
    print(message)

    client = Client(TWILIO_SID, AUTH_TOKEN)

    for article in message:
        new_message = client.messages \
            .create(
            body=article,
            from_='+12694431987',
            to='+15403706668',
        )




"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

