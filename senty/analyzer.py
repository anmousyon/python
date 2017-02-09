'''analyzer class'''

from textblob import TextBlob
from RAKE import Rake


class Analyzer:
    '''analyzes text for sentiment and important terms'''
    def __init__(self):
        self.filter = Rake('stoplist.txt')

    def sentiment(self, text):
        '''transform sentiment into trinary value'''
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.2:
            sentiment = "1"
        elif polarity < -0.2:
            sentiment = "-1"
        else:
            sentiment = "0"
        return sentiment

    def terms(self, text):
        '''get most important terms from text'''
        if text:
            terms = self.filter.run(text)[0][0]
        else:
            terms = ''
        return terms
