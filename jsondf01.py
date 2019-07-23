import numpy as np
import pandas as pd
# import pathlib as pl
# pl.Path.cwd()
jockeyct = pd.read_json('C:/Users/pathz/Documents/scrapy/nkc01/results01.json', encoding='utf-8')
# dfp = jockeyct[['place', 'jockey', 'placenum']]#.query('placenum < 4')
# dfp = jockeyct[['place', 'jockey', 'placenum'] and jockeyct['placenum'] < 4]
data = {}
jockeyct = pd.crosstab([jockeyct.place, jockeyct.jockey], jockeyct.placenum, margins=True)
rates = [round(100 * jockeyct[rank] / jockeyct.All, 2) for rank in range(1, 4)]
jockeyct['単勝率'], jockeyct['連対率'], jockeyct['複勝率'] = rates
data['jockeys'] = jockeyct.loc[:, [1,2,3,'単勝率', '連対率', '複勝率', 'All']].sort_values(['place',1,2,3], ascending=False)
data['jockeys'] = data['jockeys'].rename(columns={1:'1着',2:'2着',3:'3着','All':'騎乗数'})
for i, d in data['jockeys'].iterrows(): print(d)



jockeyct.query('placenum < 4').groupby(['place', 'jockey', 'placenum'])['placenum'].count().unstack().fillna(0)
jockeyct[['place', 'jockey', 'placenum']].query('placenum < 4').groupby(['place', 'jockey', 'placenum'])#.count(level='placenum')
jockeyct[['place', 'jockey', 'placenum']].query('placenum < 4').sort_values(['place', 'jockey', 'placenum']).set_index(['place', 'jockey']).apply(pd.value_counts)#.placenum.value_counts()#.nunique()#.count(level='jockey')
jockeyct.columns
jockeyct.groupby(['place', 'racenum']).jockey.groups
jockeygp = jockeyct.query('placenum < 4').groupby(['place', 'jockey']).placenum
jockeygp.count()
