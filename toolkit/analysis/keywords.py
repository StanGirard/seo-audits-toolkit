from inscriptis import get_text
import requests
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
from scipy.sparse import coo_matrix
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt
import numpy
from gensim import corpora
from gensim.models import LsiModel
import re
from googlesearch import search
import logging
import urllib


def extract_text_from_list_url(list):
        text = []
        count = 0
        for i in list:
            try:
                #html = requests.get(i).text
                html = urllib.request.urlopen(i, timeout=3).read().decode("utf8")
                text.append(get_text(html))
                count += 1
            except Exception as e:
                print(e)
        return text

def normalize_text_list( textArray, new_stopwords_list):
    corpus = []
    for i in range(len(textArray)):
        #Remove accents
        text = re.sub("'","  ", textArray[i])

        text = re.sub('"'," ", text)

        # Removes urls
        text = re.sub("/(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])/igm", " ", text)

        #text = str(unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore'))

        #Remove Special characters
        #text = re.sub('[^a-zA-Z0-9]', ' ', text)
        text = re.sub('[^a-zA-Z0-9áéèíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇû: ]', ' ', text)
        
        #Convert to lowercase
        text = text.lower()
        
        #remove tags
        text = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
        
        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)
        
        ##Convert to list from string
        text = text.split()
        
        ##Stemming
        #ps=PorterStemmer()
        #Lemmatisation
        #lem = WordNetLemmatizer()
        text = [word for word in text if not word in  
                new_stopwords_list] 
        text = " ".join(text)
        corpus.append(text)
    return corpus



def get_top_n_ygrams_words(corpus,stopwords, n=None, y=1):
    vec = CountVectorizer(min_df = 0.1,stop_words=stopwords, max_features=10000, ngram_range=(y,y)).fit(corpus)
    bag_of_words  = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                    reverse=True)
    frame =  pd.DataFrame(words_freq[:n])
    switcher = {
    1: "Monogram",
    2: "Bigram",
    3: "Trigram",
    }
    switcherFreq = {
    1: "Freq_Mono",
    2: "Freq_Bi",
    3: "Freq_Tri",
    }
    frame.columns = [switcher.get(y), switcherFreq.get(y)]
    dict_from_pd = frame.to_dict("index")
    list_values = []
    for i in dict_from_pd:
        list_values.append({"keyword": dict_from_pd[i][switcher.get(y)], "frequency": dict_from_pd[i][switcherFreq.get(y)]})
    return list_values
    

    


def get_all_ygrams(corpus, stopwords, monograms, bigrams, trigrams):
    mono = get_top_n_ygrams_words(corpus, stopwords,monograms, 1)
    bi = get_top_n_ygrams_words(corpus, stopwords,bigrams, 2)
    tri = get_top_n_ygrams_words(corpus, stopwords,trigrams, 3)
    all = {}
    all["Monogram"] = mono
    all["Bigram"] = bi
    all["Trigram"] = tri
    return all

def get_urls_from_query( query, number = 50, lang = 'en', tld = 'com'):
    my_results_list = []
    lang = lang
    tld = tld
    if lang is None:
        lang = 'en'
    if tld is None:
        tld = 'com' 

    for i in search(query,        # The query you want to run
                    tld = 'com',  # The top level domain
                    lang = 'en',  # The language
                    num = 10,     # Number of results per page
                    start = 0,    # First result to retrieve
                    stop = number,  # Last result to retrieve
                    pause = 2.0,  # Lapse between HTTP requests
                ):
        my_results_list.append(i)
        logging.debug(str(my_results_list.index(i)) + ": " + str(i))
    return my_results_list

def generate_results(query, number=50):
    stop = ['pouvez','permet','très','être','mentions','dune','dit','com','min','bonjour','cest', 'jai','voir', 'co','avis','faut','dun','a','abord','afin','ah','ai','aie','ainsi','allaient','allo','allons','apres','assez','attendu','au','aucun','aucune','aujourd','aujourdhui','auquel','aura','auront','aussi','autre','autres','aux','auxquelles','auxquels','avaient','avais','avait','avant','avec','avoir','ayant','b','bah','beaucoup','bien','bigre','boum','bravo','brrr','c','ca','car','ce','ceci','cela','celle','celle-ci','celle','celles','celles-ci','celles-la','celui','celui-ci','celui-la','cent','cependant','certain','certaine','certaines','certains','certes','ces','cet','cette','ceux','ceux-ci','ceux-la','chacun','chaque','cher','chere','cheres','chers','chez','chiche','chut','ci','cinq','cinquantaine','cinquante','cinquantieme','cinquieme','clac','clic','combien','comme','comment','compris','concernant','contre','couic','crac','d','da','dans','de','debout','dedans','dehors','dela','depuis','derriere','des','desormais','desquelles','desquels','dessous','dessus','deux','deuxieme','deuxiemement','devant','devers','devra','different','differente','differentes','differents','dire','divers','diverse','diverses','dix','dix-huit','dixieme','dix-neuf','dix-sept','doit','doivent','donc','dont','douze','douzieme','dring','du','duquel','durant','e','effet','eh','elle','elle-meme','elles','elles-memes','en','encore','entre','envers','environ','es','est','et','etant','etaient','etais','etait','etant','etc','ete','etre','eu','euh','eux','eux-memes','excepte','f','façon','fais','faire','faisaient','faisant','fait','feront','fi','flac','floc','font','g','gens','h','ha','he','hein','helas','hem','hep','hi','ho','hola','hop','hormis','hors','hou','houp','hue','hui','huit','huitieme','hum','hurrah','i','il','ils','importe','j','je','jusqu','jusque','k','l','la','laquelle','las','le','lequel','les','lesquelles','lesquels','leur','leurs','longtemps','lorsque','lui','lui-meme','m','ma','maint','mais','malgre','me','meme','memes','merci','mes','mien','mienne','miennes','miens','mille','mince','moi','moi-meme','moins','mon','moyennant','n','na','ne','neanmoins','neuf','neuvieme','ni','nombreuses','nombreux','non','nos','notre','notres','nous','nous-memes','nul','o','o|','oh','ohe','ole','olle','on','ont','onze','onzieme','ore','ou','ouf','ouias','oust','ouste','outre','p','paf','pan','par','parmi','partant','particulier','particuliere','particulierement','pas','passe','pendant','personne','peu','peut','peuvent','peux','pff','pfft','pfut','pif','plein','plouf','plus','plusieurs','plutot','pouah','pour','pourquoi','premier','premiere','premierement','pres','proche','psitt','puisque','q','qu','quand','quant','quanta','quant-a-soi','quarante','quatorze','quatre','quatre-vingt','quatrieme','quatriemement','que','quel','quelconque','quelle','quelles','quelque','quelques','quelquun','quels','qui','quiconque','quinze','quoi','quoique','r','revoici','revoila','rien','s','sa','sacrebleu','sans','sapristi','sauf','se','seize','selon','sept','septieme','sera','seront','ses','si','sien','sienne','siennes','siens','sinon','six','sixieme','soi','soi-meme','soit','soixante','son','sont','sous','stop','suis','suivant','sur','surtout','t','ta','tac','tant','te','tel','telle','tellement','telles','tels','tenant','tes','tic','tien','tienne','tiennes','tiens','toc','toi','toi-meme','ton','touchant','toujours','tous','tout','toute','toutes','treize','trente','tres','trois','troisieme','troisiemement','trop','tsoin','tsouin','tu','u','un','une','unes','uns','v','va','vais','vas','ve','vers','via','vif','vifs','vingt','vivat','vive','vives','vlan','voici','voila','vont','vos','votre','votre','votres','vous','vous-memes','vu','w','x','y','z','zut']
    stop_words = set(stopwords.words("french"))
    stop_words_english = set(stopwords.words("english"))
    stop_words_multilingual = stop_words.union(stop_words_english)
    new_stopwords_list = stop_words_multilingual.union(stop)

    urls = get_urls_from_query(query, number)
    tex = extract_text_from_list_url(urls)
    corpus = normalize_text_list(tex, new_stopwords_list)
    results = get_all_ygrams(corpus,new_stopwords_list, 40, 20, 10)
    return results


    
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

    results = get_urls_from_query("parse xml response python", number=10)
    print(generate_results(results))