# %%
from elasticsearch import Elasticsearch
import settings
import logging

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)

# Elasticsearchクライアント作成
es = Elasticsearch(settings.ES_URL)

# es = Elasticsearch(
#     f"http://{settings.ES_HOST}:{settings.ES_PORT}",
#     http_auth=(settings.ES_USERID, settings.ES_PASSWORD)
# )

# %%
# インデックス一覧の取得
indices = es.cat.indices(index='*', h='index').splitlines()
# インデックスの表示
for index in indices:
    logging.info(f'{index=}')

logging.info(es.indices.get_mapping(index=".kibana-event-log-7.11.2-000001"))

# クエリ
query = {
    "query": {
    "match_all": {}
  }
}

# ドキュメントを検索
result = es.search(index=".kibana-event-log-7.11.2-000001", body=query, size=3)
# 検索結果からドキュメントの内容のみ表示
for document in result["hits"]["hits"]:
    logging.info(document["_source"])

logging.info(es.get_source(index=".kibana-event-log-7.11.2-000001", id="q5yYJXgBhEZYJc86DPOw"))

logging.info(es.count(index=".kibana-event-log-7.11.2-000001"))

# es.indices.create(index='nkday')
# student = {
#     "name": "Taro",
#     "age": 36,
#     "email": "taro@example.com"
# }
# es.create(index='students', body=student)

# %%
es.close()