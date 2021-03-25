# %%

import requests
import pandas as pd
# import json

query = """query MyQuery {
  races(order_by: {place: asc, racenum: asc}) {
    raceid
    place
    racenum
    title
    coursetype
    distance
    courseinfo1
    courseinfo2
    jrarecord {
      time
    }
    weather
    condition
    datetime
    date
    posttime
    racegrade
    starters
    addedmoneylist
    requrl
    horseresults(order_by: {ranking: asc}) {
      ranking
      postnum
      horsenum
      horsename
      horseurl
      sex
      age
      jockeyweight
      jockey
      jockeyurl
      time
      margin
      fav
      odds
      last3f
      passageratelist
      affiliate
      trainer
      trainerurl
      horseweight
      horseweightdiff
    }
    paybacks {
      tansho
      tanshofav
      tanshopay
      fukusho
      fukushofav
      fukushopay
      wakuren
      wakurenfav
      wakurenpay
      umaren
      umarenfav
      umarenpay
      wide
      widefav
      widepay
      umatan
      umatanfav
      umatanpay
      fuku3
      fuku3fav
      fuku3pay
      tan3
      tan3fav
      tan3pay
    }
  }
}"""

url = 'http://localhost:8360/v1/graphql'
r = requests.post(url, json={'query': query})
print(r.status_code, '\n')
print(r.headers, '\n')
print(r.text[:600], '\n')

# json_data = json.loads(r.text)
# df_data = json_data['data']
df = pd.DataFrame(r.json()['data'])

print(df.iloc[0,:])
# %%
