# import numpy as np
import pandas as pd

racesdf = pd.read_json('C:/Users/pathz/Documents/scrapy/nkc01/results01.json', encoding='utf-8')
# racesdf = racesdf.drop('requrl', axis=1)
racesgp = racesdf[racesdf['placenum'] < 4].groupby(['place', 'racenum', 'raceid', 'title', 'courcetype', 'distance', 'weather', 'condition', 'direction', 'posttime', 'date', 'racegrade', 'starters', 'raceaddedmoney'])
racesgp = racesgp.agg(list)
racesgp.index[0]
racesgp.columns
racesgp.iloc[0]

# dfp = jockeyct[['place', 'jockey', 'placenum']]#.query('placenum < 4')
# dfp = jockeyct[['place', 'jockey', 'placenum'] and jockeyct['placenum'] < 4]
data = {}
jockeyct = pd.crosstab([racesdf.place, racesdf.jockey], racesdf.placenum, margins=True)
rates = [round(100 * jockeyct[rank] / jockeyct.All, 2) for rank in range(1, 4)]
jockeyct['単勝率'], jockeyct['連対率'], jockeyct['複勝率'] = rates
jockeyct = jockeyct[[1,2,3, '単勝率', '連対率', '複勝率', 'All']].sort_values(['place',1,2,3], ascending=False)
lastplace = ''
lastindex = ''
for index in jockeyct.index:
    if index[0] != lastplace:
        jockeyct.at[index, 'dispmode'] = 'place1st'
        jockeyct.at[lastindex, 'dispmode'] = 'placelast'

    lastplace = index[0]
    lastindex = index

jockeyct = jockeyct.drop([('All',), ('',)])
jockeyct

racesdf['racerank'] = racesdf[['place', 'racenum', 'placenum']].groupby(['place', 'racenum']).rank()
racesdf.loc[racesdf['racerank'] < 4].groupby(['place', 'racenum'])['horsename'].apply(list)

for col, row in jockeyct.iterrows():
    print(col)

jockeyct.iloc[0]
data['jockeys'] = jockeyct.rename(columns={1:'1着',2:'2着',3:'3着','All':'騎乗数'})
data['jockeys']
for th in data['jockeys'].columns:
    print(th)

data['jockeys']['1着']

for index, row in data['jockeys'].iterrows():
    print(row)

d.name
i[0]



jockeyct.query('placenum < 4').groupby(['place', 'jockey', 'placenum'])['placenum'].count().unstack().fillna(0)
jockeyct[['place', 'jockey', 'placenum']].query('placenum < 4').groupby(['place', 'jockey', 'placenum'])#.count(level='placenum')
jockeyct[['place', 'jockey', 'placenum']].query('placenum < 4').sort_values(['place', 'jockey', 'placenum']).set_index(['place', 'jockey']).apply(pd.value_counts)#.placenum.value_counts()#.nunique()#.count(level='jockey')
jockeyct.columns
jockeyct.groupby(['place', 'racenum']).jockey.groups
jockeygp = jockeyct.query('placenum < 4').groupby(['place', 'jockey']).placenum
jockeygp.count()
