import json
import requests
from tqdm.auto import tqdm
import matplotlib.pylab as plt
import csv
url = "https://api.wellcomecollection.org/catalogue/v2/images"
from collections import Counter
from collections import OrderedDict

results = {}

def plt_csv(file ,xlabel,ylabel, ytype: type, xtype:type, min, plotf):
    xy = OrderedDict()
    x = []
    y = []
    with open(file,'r') as csvfile: 
        plots = csv.reader(csvfile, delimiter = ',') 
        
        for row in plots: 
        
            if not not row and ytype(row[1]) > min:
                xy[ytype(row[1])] =  xtype(row[0])
    for key, value in xy.items() :
        x.append(value)
        y.append(key)
    plotf(  x,y, color = 'g', label = ylabel) 

    plt.xlabel(xlabel) 
    plt.ylabel(ylabel) 
    plt.xticks(rotation=70)
    plt.legend() 
    plt.show() 

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
""" 
plt_csv('years.csv', "Year", "Number of Images", int, int, 0, plt.bar)
plt_csv("genres.csv", "Genre", "Number of Images", int, str, 5, plt.barh)