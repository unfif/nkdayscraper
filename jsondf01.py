import numpy as np
import pandas as pd
# import pathlib as pl
# pl.Path.cwd()
df = pd.read_json('C:/Users/pathz/Documents/scrapy/nkc01/results01.json', encoding='utf-8')
# dfp = df[['place', 'jockey', 'placenum']]#.query('placenum < 4')
# dfp = df[['place', 'jockey', 'placenum'] and df['placenum'] < 4]
jockeyct = pd.crosstab([df.place, df.jockey], df.placenum, margins=True)
jockeyct['単勝率'] = round(100 * jockeyct[1] / jockeyct.All, 2)
jockeyct['連対率'] = round(100 * jockeyct[2] / jockeyct.All, 2)
jockeyct['複勝率'] = round(100 * jockeyct[3] / jockeyct.All, 2)
jockeyct.loc[:, [1,2,3,'単勝率', '連対率', '複勝率', 'All']].sort_values(['place',1,2,3], ascending=False)

df.query('placenum < 4').groupby(['place', 'jockey', 'placenum'])['placenum'].count().unstack().fillna(0)
df[['place', 'jockey', 'placenum']].query('placenum < 4').groupby(['place', 'jockey', 'placenum'])#.count(level='placenum')
df[['place', 'jockey', 'placenum']].query('placenum < 4').sort_values(['place', 'jockey', 'placenum']).set_index(['place', 'jockey']).apply(pd.value_counts)#.placenum.value_counts()#.nunique()#.count(level='jockey')
df.columns
df.groupby(['place', 'racenum']).jockey.groups
jockeygp = df.query('placenum < 4').groupby(['place', 'jockey']).placenum
jockeygp.count()
