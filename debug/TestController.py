# %%
import os
os.chdir('../')#; print(os.getcwd())
from nkdayscraper.models import HorseResult
from nkdayscraper.utils.functions import getTargetDate
# from pprint import pprint
from pandas import set_option; set_option('display.max_columns', 100); set_option('display.max_rows', 500)

horseResult = HorseResult()
date = getTargetDate()
data = horseResult.getRecords(date)

# pprint(data['records'].head(1))# dict_keys(['jockeys', 'records', 'racesinfo', 'results', 'json'])
data['records'].head(1)

# %%
