from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import nltk
nltk.download('vader_lexicon')
import finnhub
import time

class StockSentiment:
    def __init__(self, api_key):
        self.api = api_key
        self.client = finnhub.Client(api_key=self.api)
        pass
    def getScoresWithDates(self, myStock, ticker, sleepTime):
        self.scores=[]
        self.dates=[]
        for date in myStock['ds']:
            try:
                date_str = pd.to_datetime(date).strftime('%Y-%m-%d')
                self.res = self.client.company_news(ticker, _from=date_str, to=date_str)
                self.sentiment_df = pd.DataFrame(self.res)
                if not self.sentiment_df.empty:
                    self.sentiment_df['datetime'] = pd.to_datetime(self.sentiment_df['datetime'], unit='h')
                    sia = SentimentIntensityAnalyzer()
                    headlines = [x['headline'] for x in self.res]
                    self.scores.append(pd.Series([sia.polarity_scores(h)['compound'] for h in headlines]).mean())
                else:
                    self.scores.append(0)
                self.dates.append(date)
            except Exception as e:
                print(f"couldn't get {date} bcoz of {e}")
                pass
            time.sleep(sleepTime)
        return pd.DataFrame({'scores' : self.scores, 'ds' : self.dates})
        
    def getScoreForSpecificDateRange(self, ticker, from_date, to_date):
        res = self.client.company_news(ticker, _from=from_date, to=to_date)
        sia = SentimentIntensityAnalyzer()
        headlines = [x['headline'] for x in res]
        self.scores = pd.Series([sia.polarity_scores(h)['compound'] for h in headlines]).mean()
        return self.scores