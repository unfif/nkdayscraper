# %%
import sys
sys.path.append('../nkdayscraper')
sys.path.append('/Users/pathz/Documents/scrapy/nkdayscraper')
from nkdayscraper.models import HorseResult
from nkdayscraper.utils.functions import getTargetDate
import logging

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)

# %%
horseResult = HorseResult()
date = getTargetDate()
data = horseResult.getRecords(date)
# %%
from pandas import set_option; set_option('display.max_columns', 100); set_option('display.max_rows', 500)
df = data['records']
# feature_columns = ['場所', 'R', 'タイトル', '形式', '距離', '情報1', '情報2', 'レコード', '天候', '状態', '日時', '日程', '時刻', 'グレード', '頭数', '賞金', '着順', '枠番', '馬番', '馬名', '性', '齢', '斤量', '騎手', 'タイム', '着差', '人気', 'オッズ', '上り', '通過', '所属', '調教師', '馬体重', '増減']
feature_columns = ['場所', 'R', 'タイトル', '形式', '距離', '情報1', '情報2', 'レコード', '天候', '状態', '日時', '日程', '時刻', 'グレード', '頭数', '賞金', '着順', '枠番', '馬番', '馬名', '性', '齢', '斤量', '騎手', '人気', 'オッズ', '所属', '調教師', '馬体重', '増減']
features_orig = df.query("着差 not in ('除外', '中止', '取消') and 着順 <= 8")[feature_columns]
labels = features_orig['着順']
# %%
from sklearn.preprocessing import LabelEncoder
lb = LabelEncoder()
encoding_columns = ['場所', 'タイトル', '形式', '情報1', '情報2', 'レコード', '天候', '状態', '日時', '日程', '時刻', 'グレード', '賞金', '馬名', '性', '齢', '騎手', '所属', '調教師']
features = features_orig
for encoding_column in encoding_columns:
    features[encoding_column] = lb.fit_transform(features_orig[encoding_column])

# %%
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size = 0.5, random_state = 0)
print(features_train.shape, features_test.shape, labels_train.shape, labels_test.shape)
# %%
from sklearn import svm
Linsvc = svm.LinearSVC(max_iter = 3000, random_state = 0)
Linsvc.fit(features_train, labels_train)
# %%
labels_pred_Linsvc = Linsvc.predict(features_test)
print(str(labels_pred_Linsvc).replace('\n', '')[:172])
print(str(list(features_test['着順'])).replace(',', '')[:172])
# %%
