import requests
import math

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_URL = 'https://www.alphavantage.co/query'

NEWS_URL = 'https://newsapi.org/v2/everything'

stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': API_KEY,
}

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_response = requests.get(url=STOCK_URL, params=stock_parameters)
data = stock_response.json()['Time Series (Daily)']
print(data)

required_dates = dict(list(data.items())[0:2])
required_dates_list = list(required_dates)

yesterday_date = required_dates_list[0]
day_before_date = required_dates_list[1]

yesterday_close = required_dates[yesterday_date]['4. close']
print(yesterday_close)

day_before_close = required_dates[day_before_date]['4. close']
print(day_before_close)

difference = float(yesterday_close) - float(day_before_close)
percent = math.ceil((difference / float(yesterday_close)) * 100)

if difference > 0:
    up_down = '🔺'
elif difference < 0:
    up_down = '🔻'


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if abs(percent) > 1:
    news_parameters = {
        'apikey': API_KEY,
        'qInTitle': COMPANY_NAME,
    }

news_response = requests.get(url=NEWS_URL, params=news_parameters)
content = news_response.json()['articles']

news_slice = content[:3]

articles = [(f"{STOCK}: {up_down} {percent}% \nHeadline: {article['title']}. \nBrief: {article['description']}") for article in news_slice]


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

