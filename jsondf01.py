# import numpy as np
import pandas as pd

racesdf = pd.read_json('C:/Users/pathz/Documents/scrapy/nkc01/results01.json', encoding='utf-8')
comment = {'raceid':'レースID','place':'場所','racenum':'R','title':'クラス','courcetype':'形式','distance':'距離','direction':'情報','weather':'天候','condition':'状態','posttime':'時刻','date':'日程','racegrade':'グレード','starters':'頭数','raceaddedmoney':'賞金','placenum':'順位','postnum':'枠番','horsenum':'馬番','horsename':'馬名','sex':'性','age':'齢','weight':'斤量','jockey':'騎手','time':'タイム','margin':'着差','position':'通過','odds':'オッズ','fav':'人気','last3f':'上り','trainer':'調教師', 'horseweight':'馬体重','horseweightdiff':'増減'}
data = {}
data['racesdf'] = racesdf.rename(columns=comment)
# racesgp = racesdf.query('placenum < 4').groupby(['place', 'racenum', 'raceid', 'title', 'courcetype', 'distance', 'weather', 'condition', 'direction', 'posttime', 'date', 'racegrade', 'starters', 'raceaddedmoney'])
racesgp = data['racesdf'].query('順位 < 4').groupby(['場所','R','レースID','クラス','形式','距離','天候','状態','情報','時刻','日程','グレード','頭数','賞金'])
racesgp2 = racesgp.agg(list).applymap(lambda x: '[' + ', '.join(map(str, x)) + ']')
racesgp2 = racesgp2.groupby(['場所','形式']).agg(list).applymap(lambda x: '[' + ', '.join(map(str, x)) + ']')
data['racesgp2'] = racesgp2[['枠番','馬番','人気']]
data['racesgp2'].index
data['racesgp2'].columns
# racesgp.groupby(['placenum','postnum','horsenum','horsename','sex','age','weight','jockey','time','margin','fav','odds','last3f','position','trainer','horseweight','horseweightdiff','requrl']).agg(list)
racesgp.groupby(['順位','枠番','馬番','馬名','性','齢','斤量','騎手','タイム','着差','人気','オッズ','上り','通過','調教師','馬体重','増減','requrl'])
racesgp.groupby(['順位']).agg(list)
type(racesgp)


[x for x in racesgp.columns]
racesgp.index[0]
racesgp.iloc[0].index

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

racesdf['racerank'] = racesdf[['place', 'racenum', 'placenum']].groupby(['place', 'racenum']).rank()
racesdf.loc[racesdf['racerank'] < 4].groupby(['place', 'racenum'])['horsename'].agg(list)

data['jockeys'] = jockeyct.rename(columns={1:'1着',2:'2着',3:'3着','All':'騎乗数'})

"""jockeyct.query('placenum < 4').groupby(['place', 'jockey', 'placenum'])['placenum'].count().unstack().fillna(0)
jockeyct[['place', 'jockey', 'placenum']].query('placenum < 4').groupby(['place', 'jockey', 'placenum'])#.count(level='placenum')
jockeyct[['place', 'jockey', 'placenum']].query('placenum < 4').sort_values(['place', 'jockey', 'placenum']).set_index(['place', 'jockey']).apply(pd.value_counts)#.placenum.value_counts()#.nunique()#.count(level='jockey')
jockeyct.columns
jockeyct.groupby(['place', 'racenum']).jockey.groups
jockeygp = jockeyct.query('placenum < 4').groupby(['place', 'jockey']).placenum
jockeygp.count()"""
