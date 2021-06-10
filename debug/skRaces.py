# %%
import sys
sys.path.append('../nkdayscraper')
sys.path.append('/Users/pathz/Documents/scrapy/nkdayscraper')
from nkdayscraper.models import Race
from nkdayscraper.utils.functions import getTargetDate
import logging

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)

# %%
race = Race()
data = race.getRecords()
from pandas import set_option; set_option('display.max_columns', 100); set_option('display.max_rows', 500)
df = data['records']
# %%
feature_columns = ['年', '場所', 'R', 'タイトル', '形式', '距離', '情報1', '情報2', '天候', '状態', '日時', '日程', '時刻', '世代', '頭数']
features_orig = df[feature_columns]
# %%
from sklearn.preprocessing import LabelEncoder
lb = LabelEncoder()
encoding_columns = ['場所', 'タイトル', '形式', '情報1', '情報2', '天候', '状態', '日時', '日程', '時刻', '世代']
features = features_orig
for encoding_column in encoding_columns:
    features[encoding_column] = lb.fit_transform(features_orig[encoding_column])

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5)
clusters = kmeans.fit(features)
df['cluster'] = clusters.labels_

print(df.query('cluster == 0').head(50))
# %%
