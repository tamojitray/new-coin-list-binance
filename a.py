import requests
import json
from bs4 import BeautifulSoup
import datetime
import time
import re

start1 = time.time()

# Make a request to the page and get the HTML content
url = "https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48"
response = requests.get(url)
html_content = response.content

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the script tag with ID "__APP_DATA" and extract its content
script_tag = soup.find('script', id='__APP_DATA')
script_content = script_tag.string

# Convert the script content to a JSON object
json_data = json.loads(script_content)

#Testing with custom json data
#with open('data.json') as json_file:
 #json_data = json.load(json_file)

newdate = 0
#Scrap all the news
for n in range(19,-1,-1):
 coin = json_data['routeProps']['ce50']['catalogs'][0]['articles'][n]['title']

 #Scrap only the new listing
 if 'Binance Will List' in coin:

  #Extract only the coin Symbol
  start = '('
  end = ')'
  s = coin
  symbol=s[s.find(start)+len(start):s.rfind(end)]

  date = json_data['routeProps']['ce50']['catalogs'][0]['articles'][n]['releaseDate']

  #Scrap only the latest  
  if date > newdate:
   newdate=date

   #print(symbol)
   #Unix date to regular date format
   #timestamp_with_ms = date
   #dt = datetime.datetime.fromtimestamp(timestamp_with_ms / 1000)
   #formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]   
   #print(coin,formatted_time)

# Print the JSON object
#print(json_data)

#Save the JSON object file
#with open('data.json', 'w') as json_file:
 #json.dump(json_data, json_file)
 
print(symbol)

end1 = time.time()
total_time = end1 - start1
print("\n"+ str(total_time))