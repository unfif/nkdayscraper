# import numpy as np
import pandas as pd

racesdf = pd.read_json('C:/Users/pathz/Documents/scrapy/nkc01/results01.json', encoding='utf-8')
jplabels = {'raceid':'レースID','place':'場所','racenum':'R','title':'クラス','courcetype':'形式','distance':'距離','direction':'情報','weather':'天候','condition':'状態','posttime':'時刻','date':'日程','racegrade':'グレード','starters':'頭数','raceaddedmoney':'賞金','placenum':'順位','postnum':'枠番','horsenum':'馬番','horsename':'馬名','sex':'性','age':'齢','weight':'斤量','jockey':'騎手','time':'タイム','margin':'着差','position':'通過','odds':'オッズ','fav':'人気','last3f':'上り','trainer':'調教師', 'horseweight':'馬体重','horseweightdiff':'増減'}
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
jockeyct = jockeyct.rename(columns={1:'1着',2:'2着',3:'3着','All':'騎乗数'})
jockeysindex = list(jockeyct.columns)
jockeysindex.remove('騎乗数')
jockeysindex.insert(0,'騎乗数')
data['jockeys'] = jockeyct[jockeysindex]

data['racesdf'] = racesdf.rename(columns=jplabels)

racesgp = data['racesdf']
racesgp['R2'] = racesgp.R
racesgp = racesgp.query('順位 < 4').groupby(['場所','R','レースID','クラス','形式','距離','天候','状態','情報','時刻','日程','グレード','頭数','賞金'])
racesgp2 = racesgp.agg(list)
racesgp2.R2 = racesgp2.R2.apply(set)
racesgp2 = racesgp2.applymap(lambda x: '(' + ', '.join(map(str, x)) + ')')
racesgp2 = racesgp2.groupby(['場所','形式']).agg(list).applymap(lambda x: '[' + ', '.join(map(str, x)) + ']')
racesgp2 = racesgp2.applymap(lambda x: x.strip('['']'))
racesgp2.R2 = racesgp2.R2.apply(lambda x: x.replace('(', '').replace(')', ''))
racesgp2['場所形式'] = data['racesgp2'].index
data['racesgp2'] = racesgp2[['R2','枠番','馬番','人気','騎手','場所形式']].rename(columns={'R2':'R'})
