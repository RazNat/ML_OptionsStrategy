import pandas as pd

df = pd.read_csv('/Users/rajatnathan/Desktop/UnderlyingOptionsEODCalcs_Test.csv')

df1 = df[(df['delta_1545'] < .7) & (df.option_type.isin(['C']))]
df1['date'] = pd.to_datetime(df1['quote_date'])
#df1['Month'] = df1['date'].dt.strftime('%b')
#df1['Day'] = df1['date'].dt.day
df2 = df1.set_index(['date']).sum(level=[0]).reset_index()
dfc = df1.set_index(['date']).mean(level=[0]).reset_index()
df2['C_bid-ask']= df2.bid_size_1545 - df2.ask_size_1545
df2['avgclose'] = dfc.active_underlying_price_1545 


df3 = df[(df['delta_1545'] > -.7) & (df.option_type.isin(['P']))]
df3['date'] = pd.to_datetime(df3['quote_date'])
#df3['Month'] = df3['date'].dt.strftime('%b')
#df3['Day'] = df3['date'].dt.day
df4 = df3.set_index(['date']).sum(level=[0]).reset_index()
df4['P_bid-ask']= df4.bid_size_1545 - df4.ask_size_1545

df5 = df2[['date','avgclose']]
df5['tradevoldiff']= df2.trade_volume - df4.trade_volume
df5['OIdiff']= df2.open_interest - df4.open_interest
df5['bidaskdiff']= df2['C_bid-ask'] - df4['P_bid-ask']
df5.sort_values(by=['date'], inplace=True, ascending=False)
df5['lagtradevoldiff'] = df5['tradevoldiff'].shift(-1)
df5['lagOIdiff'] = df5['OIdiff'].shift(-1)
df5['lagbidaskdiff'] = df5['bidaskdiff'].shift(-1)


df5.to_csv('/Users/rajatnathan/Desktop/UnderlyingOptionsEODCalcs_TrainingOUTtest.csv', sep='\t', encoding='utf-8',index=False)




