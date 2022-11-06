import pandas as pd
import csv
import numpy as np
import math


with open ('/Users/rajatnathan/Desktop/Python/UnderlyingOptionsTradesCalcs_2019-04.csv') as infile: #--change filename here
    reader = csv.reader(infile)
    headers = next(reader)
header_indices = [i for i, item in enumerate(headers) if item]

df = pd.read_csv('/Users/rajatnathan/Desktop/Python/UnderlyingOptionsTradesCalcs_2019-04.csv', usecols = header_indices) #--change filename here


# -- enter position

df_0 = df
df_0[['date','time']] = df_0['quote_datetime'].str.split(expand=True)
df_0['date_s'] = pd.to_datetime(df_0.pop('date'), format='%Y/%m/%d')
df_0['time_s'] =  pd.to_datetime(df_0.pop('time'))

df_1 = df_0.set_index(['time_s']).between_time('10:05:00', '10:06:00').reset_index()
df_2 = df_1.set_index(['date_s']).mean(level=[0])

df_2['avgopen'] = (df_2['underlying_bid'] + df_2['underlying_ask'])/2


# -- close position

df_a = df
df_a[['date','time']] = df_a['quote_datetime'].str.split(expand=True)
df_a['date_s'] = pd.to_datetime(df_a.pop('date'), format='%Y/%m/%d')
df_a['time_s'] =  pd.to_datetime(df_a.pop('time'))

df_b = df_a.set_index(['time_s']).between_time('15:56:00', '16:00:00').reset_index()
df_c = df_b.set_index(['date_s']).mean(level=[0])

df_c['avgclose'] = (df_c['underlying_bid'] + df_c['underlying_ask'])/2


# -- exit position
df_3 = df
df_3[['date','time']] = df_3['quote_datetime'].str.split(expand=True)
df_3['date_s'] = pd.to_datetime(df_3.pop('date'), format='%Y/%m/%d')
df_3['time_s'] = pd.to_datetime(df_3.pop('time'))

df_4 = df_3.set_index(['time_s']).between_time('10:07:00', '15:55:00').reset_index()

df_5 = df_4.sort_values(['date_s','time_s'])

out_dt = ''

df_6 = pd.DataFrame(columns = ['Date','Exit_Type_UP','Exit_Type_DWN','Exit_Time','FE_pricediff']) # -- shell dataframe does not need to be adjusted for size
j=0 
m=15 #-- can change threshold
c=-15 #-- can change threshold

for i in range (0,len(df_5)-1):                    
    
    x = df_5.iat[i,25]
    y = df_5.iat[i+1,25]# -- date_s (check next date)
    z = ((df_5.iat[i,17] + df_5.iat[i,18])/2)- df_2.at[x,'avgopen'] # -- price change underlying
        
    while x != out_dt:

        if x==y:
                    
            if z>= m: #-- can change threshold
                
                df_6.at[j,'Date'] = x
                time_exit = df_5.iat[i,0]
                df_6.at[j,'Exit_Time']=time_exit
                df_6.at[j,'Exit_Type_UP']=1
                #df_6.at[j,'Exit_Type_DWN']=0
                df_6.at[j,'FE_pricediff'] = m #--chnage threshold here
                out_dt = x
                j+=1
                break
                                
            else:
            
                break

        elif x!=y or i==len(df_5)-1:
        
            df_6.at[j,'Date'] = x
            df_6.at[j,'Exit_Time']=0
            df_6.at[j,'Exit_Type_UP']=2
            #df_6.at[j,'Exit_Type_DWN']=2
            df_6.at[j,'FE_pricediff'] = df_c.at[x,'avgclose'] - df_2.at[x,'avgopen'] #--chnage threshold here
            out_dt = x
            j+=1
            break       

for i in range (0,len(df_5)-1):                    
    
    x = df_5.iat[i,25]
    y = df_5.iat[i+1,25]# -- date_s
    z = ((df_5.iat[i,17] + df_5.iat[i,18])/2)- df_2.at[x,'avgopen'] # -- price change underlying
        
    while x != out_dt:

        if x==y:
                    
            if z<= c: #-- can change threshold
                
                df_6.at[j,'Date'] = x
                time_exit = df_5.iat[i,0]
                df_6.at[j,'Exit_Time']=time_exit
                #df_6.at[j,'Exit_Type_UP']=0
                df_6.at[j,'Exit_Type_DWN']=-1
                df_6.at[j,'FE_pricediff'] = c #--chnage threshold here
                out_dt = x
                j+=1
                break

            else:
            
                break

        elif x!=y or i==len(df_5)-1:
        
            df_6.at[j,'Date'] = x
            df_6.at[j,'Exit_Time']=0
            #df_6.at[j,'Exit_Type_UP']=2
            df_6.at[j,'Exit_Type_DWN']=3
            df_6.at[j,'FE_pricediff'] = df_c.at[x,'avgclose'] - df_2.at[x,'avgopen'] #--chnage threshold here
            out_dt = x
            j+=1
            break       



df_6.Date = pd.to_datetime(df_6['Date'])

# -- positive sentiment

# -- Call Option trade volume calculation --

df1 = df[(df['trade_delta'] < .4) & (df.option_type.isin(['C'])) 
# & (df['trade_price'] > ((df['best_bid'] + df['best_ask'])/2))] # -- DELTA Threshold can be changed


df1[['date','time']] = df1['quote_datetime'].str.split(expand=True)
df1['date_s'] = pd.to_datetime(df1.pop('date'), format='%Y/%m/%d')
df1['time_s'] =  pd.to_datetime(df1.pop('time'))
df1.sort_values(['date_s','time_s'])


dfx = df1.set_index(['time_s']).between_time('09:30:00', '10:00:00').reset_index()# -- time threshold can be changed to a wider window

dfy = dfx.set_index(['date_s']).sum(level=[0]).reset_index()
df_y = dfy.reindex(columns = ['date_s','trade_size']).rename(columns={"trade_size":"trade_size_C_POS","date_s":"Date"})


# -- Put Option trade volume calculation --

df2 = df[(df['trade_delta'] > -.4) & (df.option_type.isin(['P'])) & (df['trade_price'] < ((df['best_bid'] + df['best_ask'])/2))] #-- DELTA Threshold can be changed

df2[['date','time']] = df2['quote_datetime'].str.split(expand=True)
df2['date_s'] = pd.to_datetime(df2.pop('date'), format='%Y/%m/%d')
df2['time_s'] = pd.to_datetime(df2.pop('time'))
df2.sort_values(['date_s','time_s'])

dfv = df2.set_index(['time_s']).between_time('09:30:00', '10:00:00').reset_index() # -- time threshold can be changed to a wider window

dfw = dfv.set_index(['date_s']).sum(level=[0]).reset_index()
df_w = dfw.reindex(columns = ['date_s','trade_size']).rename(columns={"trade_size":"trade_size_P_POS","date_s":"Date"})


# -- negative sentiment

# -- Call Option trade volume calculation --

df_1a = df[(df['trade_delta'] < .4) & (df.option_type.isin(['C'])) & (df['trade_price'] < ((df['best_bid'] + df['best_ask'])/2))] #-- DELTA Threshold can be changed


df_1a[['date','time']] = df_1a['quote_datetime'].str.split(expand=True)
df_1a['date_s'] = pd.to_datetime(df_1a.pop('date'), format='%Y/%m/%d')
df_1a['time_s'] =  pd.to_datetime(df_1a.pop('time'))
df_1a.sort_values(['date_s','time_s'])


df_xa = df_1a.set_index(['time_s']).between_time('09:30:00', '10:00:00').reset_index()# -- time threshold can be changed to a wider window

df_ya = df_xa.set_index(['date_s']).sum(level=[0]).reset_index()
df_yaa = df_ya.reindex(columns = ['date_s','trade_size']).rename(columns={"trade_size":"trade_size_C_NEG","date_s":"Date"})


# -- Put Option trade volume calculation --

df_2a = df[(df['trade_delta'] > -.4) & (df.option_type.isin(['P'])) & (df['trade_price'] > ((df['best_bid'] + df['best_ask'])/2))] #-- DELTA Threshold can be changed

df_2a[['date','time']] = df_2a['quote_datetime'].str.split(expand=True)
df_2a['date_s'] = pd.to_datetime(df_2a.pop('date'), format='%Y/%m/%d')
df_2a['time_s'] = pd.to_datetime(df_2a.pop('time'))
df_2a.sort_values(['date_s','time_s'])

df_va = df_2a.set_index(['time_s']).between_time('09:30:00', '10:00:00').reset_index() # -- time threshold can be changed to a wider window

df_wa = df_va.set_index(['date_s']).sum(level=[0]).reset_index()
df_waa = df_wa.reindex(columns = ['date_s','trade_size']).rename(columns={"trade_size":"trade_size_P_NEG","date_s":"Date"})


# -- Final Output DataFrame

df_op = df_y.merge(df_w)
df_op['tradevolPOS'] = df_op.trade_size_C_POS + df_op.trade_size_P_POS

df_opx = df_yaa.merge(df_waa)
df_opx['tradevolNEG'] = df_opx.trade_size_C_NEG + df_opx.trade_size_P_NEG

df_opz = df_op.merge(df_opx)
df_opz['Net_Sentiment'] = df_opz.tradevolPOS - df_opz.tradevolNEG

df_opz.Date = pd.to_datetime(df_opz['Date'])

df_final = df_opz.merge(df_6)

print (df_final)

df_final.to_csv('/Users/rajatnathan/Desktop/Python/Intraday_Sep19OUT.csv', sep='\t', encoding='utf-8',index=False)




