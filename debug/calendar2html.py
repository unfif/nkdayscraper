# %%
from app import DATABASE_URL
from sqlalchemy import create_engine, text, select
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import SmallInteger, Date, Boolean
import pandas as pd
import json

is_make_html = True
engine = create_engine(DATABASE_URL, echo=False, future=True)
table_name = 'racedates'
year = 2023

with engine.connect() as conn:
    conn.execute(text(f"delete from {table_name} where extract(year from date) = '{year}'"))
    conn.commit()

# %%
file_dir = 'data/json/calendar/'
for month in range(1, 13):
    file_name = f'{year}{month:02}.json'
    with open(f'{file_dir}{file_name}') as f:
        dict = json.load(f)

    if is_make_html:
        from json2html import *
        html = json2html.convert(json=dict, table_attributes='class="table table-striped table-hover table-sm w-100 mb-0"')
        head = '<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>2021-01</title><link href="../static/css/bootstrap.min.css" rel="stylesheet"><script src="../static/js/bootstrap.bundle.min.js"></script></head>'
        with open(f"{file_dir}html/{file_name.split('.')[0]}.html", mode='w') as f:
            f.write(f'{head}{html}</html>')

    import datetime as dt
    data = dict[0]['data']
    month_data = []
    for day in data:
        if day['info'][0]['race']:
            date = dt.date(year, month, int(day['date']))
            day['date'] = date
            day['weekday'] = (date.weekday() + 1) % 7
            day['is_holiday'] = day['day'].startswith('祝日')
            day.pop('day')
            day['gradeRace'] = day['info'][0]['gradeRace']
            day['option'] = day['info'][0]['option']
            day['race'] = day['info'][0]['race']
            day.pop('info')
            month_data.append(day)

    from sqlalchemy.dialects import postgresql as pg
    df = pd.DataFrame(month_data).sort_values('date')
    df.to_sql(table_name, con=engine, if_exists='replace', index=False, dtype={
        'date': Date,
        'weekday': SmallInteger,
        'is_holiday': Boolean,
        'gradeRace': pg.ARRAY(pg.JSONB),
        'option': pg.ARRAY(pg.JSONB),
        'race': pg.ARRAY(pg.JSONB)
    })
print('done.')
# %%
