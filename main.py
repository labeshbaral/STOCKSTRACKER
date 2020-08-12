

from bs4 import BeautifulSoup
import urllib.request
from tabulate import tabulate

import requests

import pandas as pd

from alpha_vantage.timeseries import TimeSeries
import time


def opener (stringer):
 list= []
 print ("\n")
 headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
 url ='https://markets.ft.com/data/equities/tearsheet/summary?s='

 url=url+stringer
 req = urllib.request.Request(url, headers=headers)

 # url opening and reading
 resp = urllib.request.urlopen(req)
 html = resp.read()
 soup = BeautifulSoup(html, 'html.parser')

 prices = soup.find_all("table", {'class': "mod-ui-table mod-ui-table--two-column"})
 values = [x.get_text() for x in prices]
 for value in values:
     pricelist.append(value)
 finder = pricelist[1]
 floatfinder = finder[pricelist[1].find("Free"):pricelist[1].find("P/E")+1]
 oustanding = finder[pricelist[1].find("Shares"):pricelist[1].find("Free")+1]
 floatfinder=floatfinder [floatfinder.find ("t")+1:floatfinder.find ("p")]
 oustanding=oustanding [oustanding.find ("g")+1:oustanding.find ("f")]
 list.append (floatfinder)
 list.append (oustanding)
 if "m" in floatfinder:
     x=float (floatfinder [0:floatfinder.find ("m")])
     if "m" in oustanding:
         y=float (oustanding [0:oustanding.find ("m")])
         list.append ((x/y)*100)


     elif "b" in oustanding:
         y = float(oustanding[0:oustanding.find("b")])
         x=x/1000
         list.append((x / y) * 100)


 if "b" in floatfinder:
     x=float (floatfinder [0:floatfinder.find ("b")])
     if "b" in oustanding:
         y=float (oustanding [0:oustanding.find ("b")])
         list.append((x / y) * 100)

     elif "m" in oustanding:
         y = float(oustanding[0:oustanding.find("m")])
         y=y/1000
         list.append((x / y) * 100)

 return list
def getprice (stringer):
 headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
 url = 'https://markets.ft.com/data/equities/tearsheet/summary?s='

 url = url + stringer
 req = urllib.request.Request(url, headers=headers)

 # url opening and reading
 resp = urllib.request.urlopen(req)
 html = resp.read()
 soup = BeautifulSoup(html, 'html.parser')

 prices = soup.find_all("span", {'class': "mod-ui-data-list__value"})
 values = [x.get_text() for x in prices]
 for value in values:
     pricepricelist.append(value)
 #print (pricepricelist)

 return pricepricelist


def getmajorstats (stringer):
 x=getprice(stringer)
 y=opener(stringer)
 headings = ["Price", "Change (D)", "Vol (D)", "Change (Y)", "Beta", "Float", "Shares Outstanding", "Percent"]
 mydata = [(x[0], x[1], x[2], x[3], x[4], y [0], y [1], y[2])]
 print ("Here is your major stock data: ")
 print (mystocks)
 print(tabulate(mydata, headers=headings, tablefmt="fancy_grid"))

def getcandles (stringer, coder):
   r = requests.get('https://finnhub.io/api/v1/stock/candle?symbol='+stringer+ '&resolution=1&from=1572651390&to=1572910590&token='+coder)
   try:
       df = pd.DataFrame(r.json ()).to_excel("candelstick.xlsx")
   except:
       print("Could not form Excel spreadsheet")
   print (r.json ())

 #finnhub_client = finnhub.Client(api_key="bso6f17rh5rctp1fspm0")
 # Stock candles
 #print(finnhub_client.stock_candles(stringer, 'D', 1590988249, 1591852249))

def getmetrics (stringer, coder):
 part= 'https://finnhub.io/api/v1/stock/metric?symbol='+stringer+'&metric=all&token='+coder
 r = requests.get(part)
 print (r.json())
 try:
     df = pd.DataFrame(r.json()).to_excel("advancedmetrics.xlsx")
 except:
     print ("Could not form Excel spreadsheet")
 keylist=list (r.json () ['metric'].keys ())
 valuelist=list (r.json () ['metric'].values ())
 for x in range (len (valuelist)):
     valuelist [x]=str (valuelist [x])
 count=1
 for x in range (len (keylist)):
     if count%4==0:
         print ("\n")
     print (keylist [x]+":",end=" ")
     print (valuelist [x], end="    ")
     count+=1

def getNewsSentiment (stringer, coder):
 print ("\n")
 part='https://finnhub.io/api/v1/news-sentiment?symbol=' +stringer+ 'token='+coder
 r = requests.get(part)
 #print (r.text)
 #df = pd.DataFrame(r.json()).to_excel("newssentiment.xlsx")
 keylist = list (r.json().keys())
 valuelist =list (r.json().values())
 for x in range(len (valuelist)):
     print("\n")
     print(keylist[x] + ":", end=" ")
     print(valuelist[x], end="    ")

def getCompanyNews (stringer, coder):
 print("\n")
 part='https://finnhub.io/api/v1/company-news?symbol=' +stringer+ '&from=2020-04-30&to=2020-05-01&token='+coder
 r = requests.get(part)
 try:
     df = pd.DataFrame(r.json()).to_excel("companynews.xlsx")
 except:
     print("Could not form Excel spreadsheet")
 for x in range(len(r.json())):
     print(r.json()[x])
     print("\n")

def getMarketNews (coder):
 r = requests.get('https://finnhub.io/api/v1/news?category=general&token='+coder)
 #print(r.json())
 try:
     df = pd.DataFrame(r.json()).to_excel("marketnews.xlsx")
 except:
     print("Could not form Excel spreadsheet")
 for x in range(len(r.json())):
     print(r.json()[x])
     print("\n")

def getstockrealtime (stringer, reciever):
 print ("\n")
 x = '1'
 while x == '1':
     api_key = 'MN4T6WKXE0QLG4WP'
     ts = TimeSeries(key=api_key, output_format='pandas')
     data, meta_data = ts.get_intraday(symbol=stringer, interval='1min', outputsize='full')
     print (data)
     close_data = data['4. close']
     percentage_change = close_data.pct_change()

     print(percentage_change)

     last_change = percentage_change[-1]

     if abs(last_change) > 0.04:
         import smtplib
         with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
             print("Alert: %d"% last_change)
             smtp.ehlo()
             smtp.starttls()
             smtp.ehlo()

             smtp.login('stocksalertsss@gmail.com', 'stocks123')

             subject = 'STOCK ALERT'
             body = stringer+' stock has exceeded a 4% change'
             msg = f'Subject: {subject}\n\n{body}'

             smtp.sendmail('stocksalertsss@gmail.com', reciever, msg)



     x=input ("\nPress 0 to quit, 1 to wait for updates for the prices: ")
     if x=='0':
         return
     else:
         print ("\nNew updates will come every minute")
         time.sleep(60)

def movingaverage (stringer,coder):
 from alpha_vantage.techindicators import TechIndicators
 import matplotlib.pyplot as plt
 api_key=coder
 ts=TimeSeries(key=api_key, output_format='pandas')
 data_ts, meta_data_ts=ts.get_intraday (symbol=stringer, interval='1min', outputsize='full')
 period=60
 ti=TechIndicators(key=api_key, output_format='pandas')
 data_ti, meta_data_ti=ti.get_sma (symbol=stringer, interval='1min', time_period=period, series_type='close')
 df1=data_ti
 #print (data_ts)
 df2=data_ts['4. close'].iloc[period-1::]
 df2.index=df1.index
 total_df=pd.concat([df1,df2],axis=1)
 print (total_df)
 total_df.plot ()
 plt.show ()

def getpricetarget (stringer, coder):
  r = requests.get("https://finnhub.io/api/v1/stock/price-target?symbol=" +stringer+ "&token="+coder)
  #df = pd.DataFrame(r.json()).to_excel("pricetarget.xlsx")
  keylist = list(r.json().keys())
  valuelist = list(r.json().values())
  for x in range(len(valuelist)):
      print("\n")
      print(keylist[x] + ":", end=" ")
      print(valuelist[x], end="    ")

def getrectrends (stringer, coder):
  r = requests.get('https://finnhub.io/api/v1/stock/recommendation?symbol='+stringer+'&token='+coder)
  try:
      df = pd.DataFrame(r.json()).to_excel("recenttrends.xlsx")
  except:
      print("Could not form Excel spreadsheet")
  for x in range (len (r.json())):
      print (r.json () [x])
      print ("\n")

pricelist =[]
pricepricelist= []
mystocks=[]

f=-1
while f!='11':
   f=input ("\nPress 1 for major stats, press 2 for general stock market news, press 3 for candelstick data, press 4 for advanced metrics, press 5 for media sentiment, press 6 for company news, \n press 7 to get real time stock data, press 8 to get a graph of the moving average, press 9 for price targets, press 10 for recent trends, press 11 to QUIT: ")
   if f=='2' or f=='3' or f=='4' or f=='6' or f=='10':
       print ("\nStatistics will be exported into an excel spreadsheet\n")
   if f=='11':
       print ("\n Done")
       break
   if f=='1':
     stringer = input("Type in the ticker for the company you want: ")
     mystocks.append(stringer)
     try:
         getmajorstats(stringer)
     except:
         print ("This data is unavailable at this time")

   if f=='2':
      coder = input("For advanced data, go to https://finnhub.io/dashboard and generate an API key; type your code below" + "\n")
      try:
          getMarketNews(coder)
      except:
          print("This data is unavailable at this time")

   if f=='3':
     stringer = input("Type in the ticker for the company you want: ")
     mystocks.append(stringer)
     coder = input("For advanced data, go to https://finnhub.io/dashboard and generate an API key; type your code below" + "\n")
     try:
         getcandles(stringer, coder)
     except:
         print("This data is unavailable at this time")

   if f=='4':
     stringer = input("Type in the ticker for the company you want: ")
     mystocks.append(stringer)
     coder = input("For advanced data, go to https://finnhub.io/dashboard and generate an API key; type your code below" + "\n")
     try:
         getmetrics(stringer, coder)
     except:
         print("This data is unavailable at this time")
   if f=='5':
     stringer = input("Type in the ticker for the company you want: ")
     mystocks.append(stringer)
     coder = input("For advanced data, go to https://finnhub.io/dashboard and generate an API key; type your code below" + "\n")
     try:
         getNewsSentiment(stringer, coder)
     except:
         print("This data is unavailable at this time")

   if f=='6':
     stringer = input("Type in the ticker for the company you want: ")
     mystocks.append(stringer)
     coder = input("For advanced data, go to https://finnhub.io/dashboard and generate an API key; type your code below" + "\n")
     try:
         getCompanyNews(stringer, coder)
     except:
         print("This data is unavailable at this time")

   if f=='7':
     stringer = input("Type in the ticker for the company you want: ")
     mystocks.append(stringer)
     reciever = input("Enter your email to receive alerts: ")
     try:
         getstockrealtime(stringer, reciever)
     except:
         print("This data is unavailable at this time")
   if f=='8':
     stringer = input("Type in the ticker for the company you want: ")
     mystocks.append(stringer)
     coder = input("For advanced data, go to https://finnhub.io/dashboard and generate a Free API key; type your code below" + "\n")
     try:
         movingaverage(stringer, coder)
     except:
         print("This data is unavailable at this time")

   if f=='9':
      stringer = input("Type in the ticker for the company you want: ")
      mystocks.append(stringer)
      coder = input("For advanced data, go to https://finnhub.io/dashboard and generate a Free API key; type your code below" + "\n")
      try:
          getpricetarget(stringer, coder)
      except:
          print("This data is unavailable at this time")

   if f=='10':
      stringer = input("Type in the ticker for the company you want: ")
      mystocks.append(stringer)
      coder = input("For advanced data, go to https://finnhub.io/dashboard and generate a Free API key; type your code below" + "\n")
      try:
          getrectrends(stringer, coder)
      except:
          print("This data is unavailable at this time")


  #print("This data is unavailable at this time")


#print (tabulate(valuelist, headers=keylist, tablefmt="fancy_grid"))


#for metric, value in r.json ()['metric'].items ():
#r=requests.get ("https://www.tiingo.com/aapl/overview")
#print (r.content)





