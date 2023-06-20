# %%
from nkdayscraper.models import HorseResult
from nkdayscraper.utils.functions import getTargetDate
import pandas as pd
# %%
pd.set_option('display.max_columns', 100); pd.set_option('display.max_rows', 500)
horseResult = HorseResult()
date = getTargetDate()
data = horseResult.getRecords(date)
records = data['records']
print(records.iloc[0, :])
print(records[[
    '場所',
    'R',
    'タイトル',
    '形式',
    '距離',
    '情報1',
    '情報2',
]].drop_duplicates())
print(data.keys())

# %%
