import json
import requests
from tqdm.auto import tqdm
import matplotlib.pylab as plt
import csv
import networkx as nx
url = "https://api.wellcomecollection.org/catalogue/v2/images"
from collections import Counter
from collections import OrderedDict
from PIL import Image
import os
import numpy as np
from itertools import chain
import seaborn as sns
from helpers import plt_csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict, Counter
import numpy as np
import pandas as pd
import jaal

# Download NLTK resources

nltk.download('punkt_tab')
nltk.download('stopwords')
genres = set()
with open("genres.csv", 'r') as csv_f :
    f = csv.reader(csv_f, delimiter = ',')
    for row in f:
        if(not not(row)):
            genres.add(str(row[0]).lower().removesuffix("s"))
response = requests.get(
        url,
        params={ "pageSize" : "100"}
                   
            
).json()
print(genres)

to_filter = set(['colour','ca','le','la','des','de','du','coloured','sur',"les","et","en","avec","par", ])
co_occurrences = defaultdict(Counter)
occurrences = {}
for k in response["results"] : 
    q = k["source"]["title"]
    
    if not (not q) :
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(q.lower())
        words = [word for word in words if word.isalnum() and word not in stop_words and word not in genres and word not in to_filter]   
       
        for i, word in enumerate(words):
            a = occurrences.get(word)
            if (a  != None) : 
                occurrences.update({word: a + 1})
            else:
                occurrences.update({word: 1})
                    
            for j in range( i , len(words)):
                if i != j:
                    co_occurrences[word][words[j]] += 1 
                
                    
                
                     
while "nextPage" in response:
    print("a")
    response = requests.get(response["nextPage"]).json()
    
    if "errorType" not in response :
        for k in response["results"] : 
            q = k["source"]["title"]
            stop_words = set(stopwords.words('english'))
            words = word_tokenize(q.lower())
            words = [word for word in words if word.isalnum() and word not in stop_words and word not in genres and word not in to_filter]   
        
            for i, word in enumerate(words):
                a = occurrences.get(word)
                if (a  != None) : 
                    occurrences.update({word: a + 1})
                else:
                    occurrences.update({word: 1})
                        
                for j in range( i , len(words)):
                    if i != j:
                        co_occurrences[word][words[j]] += 1 
occurrences2 = {}  
G = nx.Graph()    
for a,b in occurrences.items() :
    if(b>=50):
       occurrences2.update({a:b})
for a,b in occurrences2.items():
    for i,j in co_occurrences[a].items():
       
        if(occurrences2.get(i)!= None and a!=i and j>8):
            G.add_edge(a,i, weight=j)
print(G.nodes.items())
shortestPaths = dict(nx.all_pairs_shortest_path(G,2))

#print(shortestPaths.get("aids").keys())
#print(shortestPaths.get("aids"))
t = sorted(G.degree, key = lambda x : x[1])



cliques = list(nx.find_cliques_recursive(G))
eightCliques = list(filter(lambda x : len(x)>= 7 and  "les" not in x and 'lithograph' not in x, cliques))
print(eightCliques)
df = nx.to_pandas_edgelist(G)
df.columns = ["from", "to", "weight"]
jaal.Jaal(df).plot()
ax = plt.gca()
ax.margins(0.08)
plt.axis("off")

#
#plt.show()

          
        
                  
          


