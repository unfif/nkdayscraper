import numpy as np
import pandas as pd
import pathlib as pl
df = pd.read_json('C:/Users/pathz/Documents/scrapy/nkc01/results01.json', encoding='utf-8')
df[['place', 'jockey', 'placenum']].query('placenum < 4').groupby(['place', 'jockey', 'placenum'])#.count(level='placenum')
df[['place', 'jockey', 'placenum']].query('placenum < 4').sort_values(['place', 'jockey', 'placenum']).set_index(['place', 'jockey']).apply(pd.value_counts)#.placenum.value_counts()#.nunique()#.count(level='jockey')
df.columns
df.groupby(['place', 'racenum']).jockey.groups
df.groupby(['place', 'jockey', 'placenum']).query('placenum < 4')
jockeygp = df.query('placenum < 4').groupby(['place', 'jockey']).placenum
jockeygp.count()
jockeygp[jockeygp['placenum'] < 4]
df.query('place == 福島')
