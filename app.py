from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-07-01#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('div',attrs={'class':'card-body'})
row = table.find_all('th',attrs={'scope':'row'})
row_length = len(row)
row_length
temp = [] #initiating a tuple


j = 0
#insert the scrapping process here
for i in range(1, row_length):
	
    # get judul
    period = table.find_all('th',attrs={'scope':'row'})[i].text
    
    # get marketcap
    Marketcap = table.find_all('td',attrs={'class':'text-center'})[(i+3)+j].text
    Marketcap = Marketcap.strip()
    j=j+1
    
    # get Volume
    Volume = table.find_all('td',attrs={'class':'text-center'})[(i+3)+j].text
    Volume = Volume.strip()
    j=j+1
    
    # get Open
    Open = table.find_all('td',attrs={'class':'text-center'})[(i+3)+j].text
    Open = Open.strip()
    j=j+1
    
    # get Close
    Close = table.find_all('td',attrs={'class':'text-center'})[(i+3)+j].text
    Close = Close.strip()

    
    temp.append((period,Marketcap,Volume,Open,Close))
    #scrapping process
    
temp 

# temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns=('Date','MarketCap','Volume','Open','Close'))

#insert data wrangling here
df['Date'] = df['Date'].astype('datetime64')
df['MarketCap'] = df['MarketCap'].str.replace(',','')
df['MarketCap'] = df['MarketCap'].str.replace(r'\D+','', regex=True).astype('int64')
# df['MarketCap'] = df['MarketCap'].astype('int64')

df['Volume'] = df['Volume'].str.replace(',','')
df['Volume'] = df['Volume'].str.replace(r'\D+','', regex=True).astype('int64')
# df['Volume'] = df['Volume'].astype('int64')

df['Open'] = df['Open'].str.replace(',','')
df['Open'] = df['Open'].str.replace(r'\D+','', regex=True).astype('float64')
# df['Open'] = df['Open'].astype('float64')

df['Close'] = df['Close'].str.replace(',','')
df['Close'] = df['Close'].str.replace(r'\D+','', regex=True).astype('float64')
# df['Close'] = df['Close'].astype('float64')

df = df.set_index('Date')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["Volume"].mean().round(2)}'

	# generate plot
	ax = df.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "Pergerakan Volume Etherium": 
    app.run(debug=True)
