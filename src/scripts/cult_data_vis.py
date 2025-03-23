import json
import requests
from tqdm.auto import tqdm
import matplotlib.pylab as plt
import csv

url = "https://api.wellcomecollection.org/catalogue/v2/images"
from collections import Counter
from collections import OrderedDict
from PIL import Image
import os
import numpy as np
from itertools import chain
import seaborn as sns
from helpers import plot_dict_from_csv, write_dict_to_csv

results = {}


# count for every year (1500-2021)
"""

for i in range(1500, 2022):
    response = requests.get(
        url,
        params={
            
            "source.production.dates.from" : str(i) + "-01-01",
            "source.production.dates.to" : str(i+1) + "-01-01",
            "pageSize": "100"
        },
    ).json()
    results.update({i : response["totalResults"]})
    print(i)
print(results)    
plt.plot(results.keys(), results.values())  
plt.show()
with open('years.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in results.items():
       writer.writerow([key, value])
 
#get genress :
response = requests.get(
        url,
        params={"include" :  "source.genres", "pageSize" : "100"}
                   
            
).json()

genres = []
for i in response["results"] : 
    q = i["source"]["genres"]
    if not (not q) :
        genres.append(q[0]["label"])
while "nextPage" in response:
    
    response = requests.get(response["nextPage"]).json()
    
    if "errorType" not in response :
        for i in response["results"] : 
            q = i["source"]["genres"]
            if not (not q) :
                genres.append(q[0]["label"])
        print("a")        
final_count= Counter(genres)
with open('genres.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in final_count.items():
       writer.writerow([key, value])
print(final_count)


response = requests.get(
        url,
        params={"aggregations" :  "locations.license", "pageSize" : "100"}).json()

print(response["results"])

#plot csv files
plt_csv('years.csv', "Year", "Number of Images", int, int, 0, plt.bar)
plt_csv("genres.csv", "Genre", "Number of Images", int, str, 5, plt.barh)
"""


# get resoltion of images, HAVE TO DOWNLOAD FROM NAS
IMAGE_PATH = "images"
files = os.listdir(IMAGE_PATH)
resolutions = {}
w = []
h = []
i = 0
for file in files:
    image = Image.open("images/" + file)

    # Get the size of the image
    width, height = image.size
    resolutions.update({file.removesuffix(".jpg"): (width, height)})
    w.append(width)
    h.append(height)
    i = i + 1
    print(i)
res_count = Counter(resolutions.values())


write_dict_to_csv("data/res_count_120000.csv", res_count)

plt.scatter(w, h, color="g", s=0.4)
plt.show()
plot_dict_from_csv("data/res_count_120000.csv", "count", "res", int, str, 1, plt.bar)
