import json
import requests
from tqdm.auto import tqdm
import matplotlib.pylab as plt
import csv
url = "https://api.wellcomecollection.org/catalogue/v2/images"


results = {}

# count for every year (1500-2021)

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