# %%
from sqlalchemy import create_engine, select
from sqlalchemy.future.orm import Session, aliased
import pandas as pd
import settings
from models import Race, Payback, Jrarecord, HorseResult
# import logging

engine = create_engine(settings.DATABASE_URL, echo=False, future=False)
data = {}
# sql = hrs.select().order_by(hrs.c.place, hrs.c.racenum, hrs.c.ranking)
# sql = outerjoin(hrs, jrr).select().order_by(hrs.c.place, hrs.c.racenum, hrs.c.ranking)
hrs = aliased(HorseResult, name='hrs')
jrr = aliased(Jrarecord, name='jrr')
pay = aliased(Payback, name='pay')
with Session(engine) as session:
    sql = select(
        Race.raceid, Race.place, Race.racenum, Race.title, Race.coursetype, Race.distance, Race.courseinfo1, Race.courseinfo2, jrr.time.label('record'), Race.weather, Race.condition, Race.datetime, Race.date, Race.posttime, Race.racegrade, Race.starters, Race.addedmoneylist, Race.requrl,
        hrs.ranking, hrs.postnum, hrs.horsenum, hrs.horsename, hrs.sex, hrs.age, hrs.jockeyweight, hrs.jockey, hrs.time, hrs.margin, hrs.fav, hrs.odds, hrs.last3f, hrs.passageratelist, hrs.affiliate, hrs.trainer, hrs.horseweight, hrs.horseweightdiff, hrs.horseurl, hrs.jockeyurl, hrs.trainerurl,
        pay.tansho, pay.tanshopay, pay.tanshofav, pay.fukusho, pay.fukushopay, pay.fukushofav, pay.wakuren, pay.wakurenpay, pay.wakurenfav, pay.umaren, pay.umarenpay, pay.umarenfav, pay.wide, pay.widepay, pay.widefav, pay.umatan, pay.umatanpay, pay.umatanfav, pay.fuku3, pay.fuku3pay, pay.fuku3fav, pay.tan3, pay.tan3pay, pay.tan3fav
    ).join(hrs)\
    .outerjoin(pay)\
    .outerjoin(jrr)\
    .order_by(Race.place, Race.racenum, hrs.ranking)
    print(sql)
    print()
    sql = session.query(
        Race.raceid, Race.place, Race.racenum, Race.title, Race.coursetype, Race.distance, Race.courseinfo1, Race.courseinfo2, jrr.time.label('record'), Race.weather, Race.condition, Race.datetime, Race.date, Race.posttime, Race.racegrade, Race.starters, Race.addedmoneylist, Race.requrl,
        hrs.ranking, hrs.postnum, hrs.horsenum, hrs.horsename, hrs.sex, hrs.age, hrs.jockeyweight, hrs.jockey, hrs.time, hrs.margin, hrs.fav, hrs.odds, hrs.last3f, hrs.passageratelist, hrs.affiliate, hrs.trainer, hrs.horseweight, hrs.horseweightdiff, hrs.horseurl, hrs.jockeyurl, hrs.trainerurl,
        pay.tansho, pay.tanshopay, pay.tanshofav, pay.fukusho, pay.fukushopay, pay.fukushofav, pay.wakuren, pay.wakurenpay, pay.wakurenfav, pay.umaren, pay.umarenpay, pay.umarenfav, pay.wide, pay.widepay, pay.widefav, pay.umatan, pay.umatanpay, pay.umatanfav, pay.fuku3, pay.fuku3pay, pay.fuku3fav, pay.tan3, pay.tan3pay, pay.tan3fav
    )\
    .join(hrs)\
    .outerjoin(pay)\
    .outerjoin(jrr)\
    .order_by(Race.place, Race.racenum, hrs.ranking).statement

print(sql)
# %%
with engine.connect() as conn:
    records = pd.read_sql(sql, conn)
    # if len(records) == 0: return {'records': pd.DataFrame(),'jockeys': pd.DataFrame(), 'racesgp2': pd.DataFrame()}

    records.title = records.title.apply(lambda x: x.rstrip('タイトル'))
    records.posttime = records.posttime.apply(lambda x: x.strftime('%H:%M'))
    records.time = records.time.apply(lambda x: x.strftime('%M:%S %f')[1:].rstrip('0') if x is not None else None)
    records.record = records.record.apply(lambda x: x.strftime('%M:%S %f')[1:].rstrip('0'))
    records.fav = records.fav.fillna(99).astype(int)
    records.horseweight = records.horseweight.fillna(0).astype(int)
    records.horseweightdiff = records.horseweightdiff.fillna(0).astype(int)

    records = records.sort_values(['place', 'racenum', 'ranking']).reset_index(drop=True)
    records.ranking = records[['place', 'racenum', 'ranking']].groupby(['place', 'racenum']).rank(method='dense', na_option='bottom').astype(int)
    records['last3frank'] = records[['place', 'racenum', 'last3f']].groupby(['place', 'racenum']).rank(method='dense', na_option='bottom').astype(int)

    # records['nextracerank'] = pd.concat([records.ranking[1:], records.ranking[0:1]]).reset_index(drop=True)
    # records['prevracerank'] = pd.concat([records.ranking[-1:], records.ranking[:-1]]).reset_index(drop=True)
    records.loc[records.ranking <= 3, 'rankinfo'] = 'initdisp_mid'
    # records.loc[(records.ranking <= 3) & (records.nextracerank > 3), 'rankinfo'] = 'initdisp_end'
    records.loc[records.ranking > 3, 'rankinfo'] = 'initnone_mid'
    # records.loc[records.ranking - records.prevracerank < 0, 'rankinfo'] = 'initdisp_top'
    records.loc[records.racenum.diff().fillna(12) != 0, 'rankinfo'] = 'initdisp_top'
    # records.loc[(records.ranking == 1) & (records.prevracerank == 1), 'rankinfo'] = 'initdisp_top'
    # records.loc[(records.rankinfo == 'initdisp_top') & (records.nextracerank == 1), 'rankinfo'] = 'initdisp_topend'
    # records.loc[records.nextracerank - records.ranking < 0, 'rankinfo'] = 'initnone_end'

    sql = "SELECT psat.relname as TABLE_NAME, pa.attname as COLUMN_NAME, pd.description as COLUMN_COMMENT "
    sql += "FROM pg_stat_all_tables psat, pg_description pd, pg_attribute pa "
    sql += "WHERE psat.schemaname = (select schemaname from pg_stat_user_tables where relname = 'horseresults') "
    sql += "AND psat.relname IN ('races', 'horseresults', 'jrarecords', 'paybacks') AND psat.relid=pd.objoid "
    sql += "AND pd.objsubid != 0 AND pd.objoid=pa.attrelid AND pd.objsubid=pa.attnum "
    sql += "ORDER BY pd.objsubid"

    jplabels = {}
    comments = pd.read_sql(sql, conn)

jockeyct = pd.crosstab([records.place, records.jockey], records.ranking, margins=True)
jockeyct.columns = [int(x) if type(x) is float else x for x in jockeyct.columns]
ranges = [list(range(1, x+1)) for x in range(1, 4)]
jockeyct['単勝率'], jockeyct['連対率'], jockeyct['複勝率'] = [round(100 * jockeyct[ranknum].sum(axis=1) / jockeyct.All, 1) for ranknum in ranges]

jockeyct = jockeyct[[1,2,3, '単勝率', '連対率', '複勝率', 'All']].sort_values(['place',1,2,3], ascending=False)
lastplace = ''
lastindex = ''
for index in jockeyct.index:
    if index[0] != lastplace:
        jockeyct.at[index, 'dispmode'] = 'place1st'
        jockeyct.at[lastindex, 'dispmode'] = 'placelast'

    lastplace = index[0]
    lastindex = index

jockeyct = jockeyct.drop([('All', ''), ('', '')])
for ranknum in ranges: jockeyct[ranknum] = jockeyct[ranknum].astype(int)
jockeyct = jockeyct.rename(columns={1:'1着',2:'2着',3:'3着','All':'騎乗数'})
jockeysindex = list(jockeyct.columns)
jockeysindex.remove('騎乗数')
jockeysindex.insert(0,'騎乗数')
jockeyct['騎乗数'] = jockeyct['騎乗数'].astype(int)
jockeys = jockeyct[jockeysindex].copy(deep=True)
for targetcol in ['1着', '2着', '3着', '単勝率', '連対率', '複勝率']:
    for place in jockeys.index.get_level_values(0).unique():
        tmprank = jockeys.loc[place, targetcol].rank(method='dense', ascending=False, na_option='bottom')
        tmprank.index = pd.MultiIndex.from_product([(place, ), tmprank.index])
        jockeys.loc[place, targetcol + '順'] = tmprank

    jockeys.loc[:, targetcol + '順'] = jockeys.loc[:, targetcol + '順'].astype(int)
    # jockeys[targetcol + '順'] = jockeys[targetcol + '順'].astype(int)

data['jockeys'] = jockeys

for comment in comments.loc[:, 'column_name':'column_comment'].iterrows():
    jplabels.update({comment[1].column_name: comment[1].column_comment})

jplabels.update({'record': 'レコード'})
data['records'] = records.rename(columns=jplabels).copy(deep=True)
data['racesinfo'] = pd.DataFrame({'date': records.date[0], 'places': [None]})
data['racesinfo'].loc[0, 'places'] = records.place.unique()

racesgp = data['records']
racesgp['R2'] = racesgp.R
racesgp[['グレード', '賞金', '通過']] = racesgp[['グレード', '賞金', '通過']].applymap(str)
racesgp = racesgp.query('着順 < 4').groupby(['場所','R','レースID','タイトル','形式','距離','天候','状態','情報1','日時','日程','時刻','グレード','頭数','賞金'])
racesgp2 = racesgp.agg(list)
racesgp2.R2 = racesgp2.R2.apply(set)
racesgp2 = racesgp2.applymap(lambda x: '(' + ', '.join(map(str, x)) + ')')
racesgp2 = racesgp2.groupby(['場所','形式']).agg(list).applymap(lambda x: '[' + ', '.join(map(str, x)) + ']')
racesgp2 = racesgp2.applymap(lambda x: x.strip('['']'))
racesgp2.R2 = racesgp2.R2.apply(lambda x: x.replace('(', '').replace(')', ''))
data['racesgp2'] = racesgp2[['R2','枠番','馬番','人気','騎手']].rename(columns={'R2':'R'})

jsondict = {}
for key, df in data.items():
    jsondict[key] = df.to_json(orient='table', force_ascii=False)
    # jsondict[key] = df.to_dict(orient='records')

data['json'] = jsondict

print(data)
# %%
