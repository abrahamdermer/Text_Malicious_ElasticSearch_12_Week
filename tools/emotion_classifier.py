import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


class Classification:

    @staticmethod
    def get_comp_level(comp)->str:
        if  0.5 <= comp <= 1:
            return "positive"
        if -0.5 <  comp < 0.5:
            return "neutral"
        if -0.5 >= comp > -1:
            return "negative"
        

    @staticmethod  
    def get_compound(tweet:str) -> str:
        score = SentimentIntensityAnalyzer().polarity_scores(tweet)
        return Classification.get_comp_level(score['compound'])
    

    def add_val_to_emotion_fild(documents:list[dict]):
        new = {}
        for doc in documents:
            new[doc['_id']] = Classification.get_compound(doc['_source']['text'])
        return new
        

    
# print(Classification.get_compound('sdsanddunes barbarian kkk nazi isi wirathu jvp zionazis hadhave constituent open closeted'))