import pandas as pd

df = pd.read_csv('/Users/rajatnathan/Desktop/Python/UnderlyingOptionsTradesCalcs_Train.csv')

df1 = df[(df['trade_delta'] < .7) & (df.option_type.isin(['C']))]
df1['date'] = pd.to_datetime(df1['quote_datetime'])
#df1['Month'] = df1['date'].dt.strftime('%b')
#df1['Day'] = df1['date'].dt.day
df2 = df1.set_index(['date']).sum(level=[0]).reset_index()
dfx = df2.set_index(['date']).between_time('09:30:00', '10:15:00').reset_index()
#dfc = df1.set_index(['date']).mean(level=[0]).reset_index()
#dfx['C_vol']= dfx.trade_size
#df2['avgclose'] = dfc.active_underlying_price_1545 


df3 = df[(df['trade_delta'] > -.7) & (df.option_type.isin(['P']))]
df3['date'] = pd.to_datetime(df3['quote_datetime'])
#df3['Month'] = df3['date'].dt.strftime('%b')
#df3['Day'] = df3['date'].dt.day
df4 = df3.set_index(['date']).sum(level=[0]).reset_index()
dfy = df4.set_index(['date']).between_time('09:30:00', '10:15:00').reset_index()
#dfy['P_vol']= dfy.trade_size

df5 = dfx[['date']]
df5['tradevoldiff']= dfx.trade_size - dfy.trade_size
#df5['OIdiff']= df2.open_interest - df4.open_interest
#df5['bidaskdiff']= df2['C_bid-ask'] - df4['P_bid-ask']
#df5.sort_values(by=['date'], inplace=True, ascending=False)
#df5['lagtradevoldiff'] = df5['tradevoldiff'].shift(-1)
#df5['lagOIdiff'] = df5['OIdiff'].shift(-1)
#df5['lagbidaskdiff'] = df5['bidaskdiff'].shift(-1)


df5.to_csv('/Users/rajatnathan/Desktop/Python/Intraday_TrainingOUT.csv', sep='\t', encoding='utf-8',index=False)




