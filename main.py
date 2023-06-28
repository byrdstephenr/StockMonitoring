import requests
from twilio.rest import Client


date_list = []
STOCK_NAME = "SOFI"
COMPANY_NAME = "SoFi Technologies Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_KEY = "WE7DI8SDDB0AZXIW"
stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_KEY,
}

NEWS_KEY = "91f963d55cb848ffa87cf0197bacbb90"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_PARAMS = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_KEY,
    "searchIn": "title",
    "sortBy": "relevancy",
}
twilio_acct_num = "mfsKRE1Gh3mA0rcdKOoob2M1N_JMf0mxXYMHGkFI"
SMS_ENDPOINT = "https://api.twilio.com/2010-04-01"
SMS_SID = "AC98884364643e8bd718e3e59523a6c0bc"
SMS_AUTH = "55f9743224895c5ec707aca84c2840cd"
SMS_PARAMS = {
    "post": SMS_ENDPOINT,
    "accounts": SMS_SID,

}



## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterdays_close = data_list[0]['4. close']
print(yesterdays_close)
day_before_yesterday_close = data_list[1]['4. close']
print(day_before_yesterday_close)

difference = float(yesterdays_close) - float(day_before_yesterday_close)
diff_percent = round((difference / float(yesterdays_close)) * 100)
print(diff_percent)
up_down = None
if difference > 3:
    up_down = "⬆️"
else:
    up_down = "⬇️"


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
if abs(diff_percent) > 1:
    print("Yes")
    news_request = requests.get(NEWS_ENDPOINT, NEWS_PARAMS)

    news_data = news_request.json()["articles"]
    three_article = news_data[:3]
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_article]




## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
    client = Client(SMS_SID, SMS_AUTH)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_= "+12512570292",
            to="+13073145762",
        )



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

