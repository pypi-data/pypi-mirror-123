import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import yfinance as yf
from plotly import graph_objs as go
import seaborn as sns
from IPython.display import display, Image



class crypto:
	'''
	Object that functions on processes in crypto processing
	
	
	'''
	
	def __init__(self):
		print('\nCrypto Working Space Activated...\n')
	
	
	def get_crypto_visuals(self, coin, period="5d", interval="15m", MA=False, days=[7,25,99], boll=False, boll_sma=25, save_fig=False, img_format="png"):
	
	
	
	
	   '''
	   
	   Utilizing Plotly and yfinance to make a Stock Market Coin-USD timeseries plot using Candlesticks
	   
	   
	   
	   Parameters
	     -----------------
	  
	       coin: str
	             
	                 - Symbol of Crypto coin i.e 'BTC', 'ETH', 'DOGE', 'BNB', 'SXP'
	                 - Must be currently listed on https://finance.yahoo.com/cryptocurrencies/
	  
	  
	       period: str, Default "5d"
	               
	                 - Answers the question - How far back from realtime should data be sourced?
	                 - Valid periods: '1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max'
	  
	  
	       interval: str, Default "15m"
	  
	                 - References intra-period intervals of data
	                 - Valid intervals: '1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo'
	                 - Intraday data cannot extend last 60 days
	  
	       
	       MA: bool, Default False
	            
	                 - References the plotting of the Moving Average (MA) data
	       
	  
	       
	       days: list, tuple, 1D array, Pandas Series, Set, Default = [7, 25, 99]
	   
	                 - Must be an iterable containing integer values only
	                 - The integers represent, day subsets for the Moving Average data
	             
	  
	       boll: bool, Default False
	  
	                 - References the plotting of the bollinger band
	                 - Important: • When both MA and boll are True, MA takes preference
	                              • The above algorithm is in place to avoid a rowdy chart
	  
	       boll_sma:   Integer, Default 25             
	                   
	                 - Indicates the SMA value used as a reference point for plotting the bollinger band
	       
	       
	       save_fig:   bool, Default False
	                   
	                 - Saves the plot to the current working directory
	       
	  
	       img_format: str, Default "png"
	                 - The desired image format:'png', 'jpg' or 'jpeg', 'webp', 'svg', and 'pdf'
	       
	  
	   
	   
	   Returns
	     -----------------
	        None
	        
	   
	   Examples of valid use
	     -----------------
	     >>> get_crypto_visuals("BTC")
	     >>> get_crypto_visuals("BTC", MA=True)
	     >>> get_crypto_visuals("BTC", period="10d", interval="5m", MA=True, days=[10,30,100], save_fig=True, img_format='jpeg')
	     >>> get_crypto_visuals("BTC", period="10d", interval="5m", MA=False, days=[10,30,100], boll=True)
	  
	   '''
	
	   #Error Handling
	   if coin is None: raise ValueError("coin: Symbol of Crypto coin i.e 'BTC', 'ETH', 'DOGE', 'BNB', 'SXP'\nMust be currently listed on https://finance.yahoo.com/cryptocurrencies/")
	   if not isinstance(period, str): raise TypeError('period: This parameter should be a string')
	   if not isinstance(interval, str): raise TypeError('interval: This parameter should be a string')
	   if not isinstance(img_format, str): raise TypeError('img_format: This parameter should be a string')
	   if not isinstance(coin, str): raise TypeError('coin: This parameter should be a string')
	   if not isinstance(MA, bool): raise TypeError('MA: This parameter should be boolean (True or False)')
	   if not isinstance(boll, bool): raise TypeError('boll: This parameter should be boolean (True or False)')
	   if not isinstance(save_fig, bool): raise TypeError('save_fig: This parameter should be boolean (True or False)')
	   if not isinstance(boll_sma, int): raise TypeError('boll_sma: This parameter should be an Integer')
	   if (not hasattr(days, '__iter__')) or isinstance(days, str): raise TypeError("days: This parameter should be iterable, strings aren't also allowed")
	   
	   #Saving attributes
	   self.coin = coin
	   self.period = period
	   self.interval = interval
	   self.MA = MA
	   self.days = days
	   self.boll = boll
	   self.boll_sma = boll_sma
	   self.save_fig = save_fig
	   self.img_format = img_format
	
	
	
	
	
	   coin = coin.upper().strip()
	   data = yf.download(tickers=f'{coin}-USD',period = period, interval = interval)
	   header = f"{coin}-USD Price Analysis"
	
	
	   #Generate Moving Average
	   if MA==True:
	     for i in days: data[f'MA{i}'] = data['Close'].rolling(i).mean()
	
	
	   #Generate Bollinger
	   def get_bollinger_band(prices, rate=boll_sma):
	     sma = prices.rolling(rate).mean()
	     std = prices.rolling(rate).std()
	     bollinger_up = sma + std * 2 
	     bollinger_down = sma - std * 2
	     return sma, bollinger_up, bollinger_down  
	
	   if boll:
	     if not (MA or (boll and MA)): sma, u,d = get_bollinger_band(data['Close'])
	
	   #declare figure
	   fig = go.Figure()
	
	
	   #Candlestick
	   fig.add_trace(go.Candlestick(x=data.index,
	                                open=data['Open'],
	                                high=data['High'],
	                                low=data['Low'],
	                                close=data['Close'], 
	                                name = 'Market data'))
	   #Randomly pick from preferred colors
	   col_lst = ['pink','darkgray','orange','darkblue','darkcyan','darkgoldenrod','darkgray','darkgrey','darkkhaki','darkmagenta','darkorange','darkorchid','darksalmon','darkslateblue','darkslategray','darkslategrey','darkturquoise','darkviolet','deeppink']
	   try: col_sam = random.sample(col_lst, len(days))
	   except ValueError: col_sam = np.random.choice(col_lst, len(days))
	
	
	   #Add Moving average on the chart
	   co = 0
	   for col in data.columns:
	     if col.startswith('MA'):
	       fig.add_trace(go.Scatter(x=data.index, y= data[col],line={'color':col_sam[co],'width':1.5}, name = col))
	       co+=1
	
	   #Add Bollinger on the chart
	   if boll:
	     if not (MA or (boll and MA)):
	        fig.add_trace(go.Scatter(x=data.index, y= u,line={'color':'darkmagenta','width':1.5}, name = "BOLL (Up)"))
	        fig.add_trace(go.Scatter(x=data.index, y=sma, line={'color':'orange','width':1.5}, name="BOLL (Mid)"))
	        fig.add_trace(go.Scatter(x=data.index, y= d,line={'color':'darkblue','width':1.5}, name = "BOLL (Down)"))
	
	
	   #Updating axis and graph
	   fig.update_xaxes(title=f'Datetime', rangeslider_visible =True)
	
	   fig.update_yaxes(title='USD ($)')
	   fig.update_layout({"title": {"text": header}})
	
	   #Show
	   fig.show()
	
	
	   #Save
	   if save_fig: fig.write_image("fig_timeplot_{}-usd.{}".format(coin.lower(), img_format.lower()), engine='kaleido') 
