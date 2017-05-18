import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#**********************
# variable 1 - Sell;
# Variable -1 - Buy;
# Variable 0 - Do Nothing;
# Intial Capital - 1,00,000
#**********************

def get_data():
	df = pd.read_csv("Data_Set.csv")
	df['tp'] = (df['High']+df['Low']+df['Close'])/3
	return df


def get_rolling_mean(values, window):
	return pd.rolling_mean(values, window=window)


def get_rolling_std(values, window):
	return pd.rolling_std(values,window = window)


#Bollinger Bands
def get_bollinger_bands(rm, rstd):
	upper_band = rm + 1.60*rstd
    lower_band = rm -1.60*rstd
    return upper_band, lower_band

def plot_data(df,title = "Stock Prices"):
	ax = df.plot(title = title,fontsize = 2)
	ax.set_xlabel("Date")
	ax.set_ylabel("Price")
	plt.show()


#Commodity Channel Index
def get_cci(df):
	i = 0;
	while (i < df.shape[0]): 
		df.at[i,'cci'] = (66.667)*(df.at[i,'tp']-df.at[i,'rm'])/df.at[i,'rstd']
		i = i+1;		
	return df

#def interpolate(i,df):
#	y1 = df.at[i,'Open'];
#	y2 = df.at[i,'High'];
#	y3 = df.at[i,'Close'];
	
	
	
def strategy3(df):
	i = 1;
	profit = 0;
	capital = 100000;
	stocks_number = 0;
	day_count = 0;
	#max_buy = 0;
	#min_sell = 100000;
	while(i < df.shape[0]):
		#Here with Bollinger bands!		
		if(df.at[i,'Close'] > df.at[i-1,'upper_band']):
			variable = 1;
		if(df.at[i,'Close'] < df.at[i-1,'lower_band']):
			variable = -1;
		else:
			variable = 0;
		#Now with CCi;
		if(df.at[i-1,'cci'] > 70):
			variable1 = 1;
		if(df.at[i-1,'cci'] < -70):
			variable1 = -1;
		else:
			variable1 = 0;
		if(variable == variable1):
			if(variable == 1):
				df.at[i,'Action'] = "Sell"
				capital = capital + df.at[i,'Close'];
				stocks_number = stocks_number-1;
			if(variable == -1):
				df.at[i,'Action'] = "Buy"
				capital  = capital - df.at[i,'Close'];
				stocks_number = stocks_number+1;
			if(variable == 0):
				df.at[i,'Action'] = "Do_nothing"
		if(variable != variable1):
			df.at[i,'Action'] = "Do_nothing"
		i = i+1;
	#Now subtracting the stocks we hold
	capital = capital + stocks_number*(df.at[i-1,'Close']);
	profit = capital - 100000;  ##intial capital 1 lakh
	percent_profit = profit/1000;
	return df,profit,percent_profit,stocks_number;

	
def strategy2(df):
	i = 1;
	profit = 0;
	capital = 100000;
	stocks_number = 0;
	while(i < df.shape[0]):
		if(df.at[i-1,'cci'] > 70):
			variable1 = 1;
			capital = capital + df.at[i,'Close'];
			stocks_number = stocks_number-1;
			df.at[i,'Action'] = "Sell";
		if(df.at[i-1,'cci'] < -70):
			variable1 = -1;
			df.at[i,'Action'] = "Buy";
			capital  = capital - df.at[i,'Close'];
			stocks_number = stocks_number+1;
		else:
			variable1 = 0;
			df.at[i,'Action'] = "Do_nothing";
		i = i+1;
	#Now subtracting the stocks we hold
	capital = capital + stocks_number*(df.at[i-1,'Close']);
	profit = capital - 100000;  ##intial capital 1 lakh
	percent_profit = profit/1000;
	return df,profit,percent_profit;

def strategy1(df):
	i = 1;
	profit = 0;
	capital = 100000;
	stocks_number = 0;
	while(i < df.shape[0]):
		#Here with Bollinger bands!		
		if(df.at[i,'Close'] > df.at[i-1,'upper_band']):
			variable = 1;
			capital = capital + df.at[i,'Close'];
			stocks_number = stocks_number-1;
			df.at[i,'Action'] = "Sell";
		if(df.at[i,'Close'] < df.at[i-1,'lower_band']):
			variable = -1;
			df.at[i,'Action'] = "Buy";
			capital  = capital - df.at[i,'Close'];
			stocks_number = stocks_number + 1;
		else:
			variable = 0;
			df.at[i,'Action'] = "Do_nothing";
		i = i+1;
	#Now subtracting the stocks we hold;	
	capital = capital + stocks_number*(df.at[i-1,'Close']);
	profit = capital - 100000;  ##intial capital 1 lakh
	percent_profit = profit/1000;
	return df,profit,percent_profit,stocks_number;	
	
def get_drawdown(df):
	i = 0;
	stock_max = -999999
	stock_min = 999999	
	while(i < df.shape[0]):
		if(df.at[i,'Close']< stock_min):
			stock_min = df.at[i,'Close']
		if(df.at[i,'Close']> stock_max):
			stock_max = df.at[i,'Close']
		i = i + 1
	draw_down = stock_max-stock_min
	print(draw_down)
	#return draw_down


def test_run():
        df = get_data()
	rm = get_rolling_mean(df['tp'],window = 15)
	rstd = get_rolling_std(df['tp'],window = 15)
	upper_band, lower_band = get_bollinger_bands(rm,rstd)
	df['rm'] = rm;
	df['rstd'] = rstd;
	df['upper_band'] = upper_band;
	df['lower_band'] = lower_band;	
	df_modified = get_cci(df);
	df_n,profit,percent_profit,stocks_number = strategy1(df_modified);
	#print(df_n);
        print("The profit is");
	print(profit);
	print("Percentage of profit is");
	print(percent_profit);
	print("Number");
	print(stocks_number);
	#print(df);
	j = 0;
	count = 0;
	while(j < df.shape[0]):
		if(df_n.at[j,'Action'] == 'Do_nothing'):
			count = count + 1;
		j = j+1;
	print(count)
	df_n['stamp'] = df_n['Date']+' '+df_n['Time']
	#print(df_n)
	#df_n.plot(x = 'stamp',y=['Close','rm','upper_band','lower_band'])
	#plt.show()
	
	
      
if __name__ == "__main__":
      test_run()

