# NkDayScraper
## Getting Started
1. git clone https://github.com/unfif/nkdayscraper.git
1. (Debug -> python3 app.py) -> Base.metadata.create_all(engine)
1. npm run all

## etc...

`del data/json/results01.json; scrapy crawl nkday -a date=20200315 -o data/json/results01.json --nolog`

`rm data/json/results01.json & scrapy crawl nkday -a date=20200315 -o data/json/results01.json --nolog`

`flask run --debugger --reload`

`web: flask run --host=0.0.0.0 --port=$PORT`

`$env:PYTHONPATH = "."`

`twistd web --wsgi nkcflask01.app.app --listen=tcp:5000`

`web: wistd web --wsgi nkcflask01.app.app --listen=tcp:$PORT`

________________________________________________________________________________
sudo date -s "09/29 18:01 2019"

### data/json/results01.json for scrapy
```rm data/json/results01.json & scrapy crawl nkday -o data/json/results01.json```

### data/json/es01.json for Elasticsearch
```cat data/json/jrarecords.json | sed -r 's/([0-9]{4})-([0-9]{2})-([0-9]{2})/\1\/\2\/\3/g' | jq -c '.[] | {"index": {"_index": "jrarecords"}}, .' > data/json/es01.json```
```curl -XPOST -H "Content-Type: application/x-ndjson" http://localhost:9200/_bulk --data-binary '@data/json/es01.json'```

### data/json/results02.json for mongoDB
```cat data/json/results01.json | sed -r 's/"([0-9]{4}-[0-9]{2}-[0-9]{2}) ([0-9]{2}:[0-9]{2}:[0-9]{2})"/{"\$date": "\1T\2.000+09:00"}/g' | sed -r 's/"([0-9]{4}-[0-9]{2}-[0-9]{2})"/{"\$date": "\1T00:00:00.000+09:00"}/g' > data/json/results02.json```

### data/json/es01.json for bonsai
```curl -XPOST -H "Content-Type: application/x-ndjson" https://k2mq362g48:8jejkoxzm3@bonsign-7182717687.ap-southeast-2.bonsaisearch.net:443/_bulk --data-binary @data/json/es01.json```

```curl -XGET https://k2mq362g48:8jejkoxzm3@bonsign-7182717687.ap-southeast-2.bonsaisearch.net:443/_stats```

### data/json/results02.json for mongoimport
```mongoimport --db netkeiba --collection horseresults --file data/json/results02.json --jsonArray --drop```

```mongoimport --uri "mongodb+srv://undo5:marehito@mongui-t1cam.gcp.mongodb.net/netkeiba?retryWrites=true&w=majority" --collection horseresults --file data/json/results02.json --jsonArray --drop```

### wget for race.netkeiba.com
```wget -r -l 1 -k -nc -E restrict-file-names=windows –random-wait "https://race.netkeiba.com/top/race_list_sub.html?kaisai_date=20200315"```

### wget for jra.jp/datafile/record
```wget -r -l 1 -k -nc -np -E -A html,htm,php,js,css restrict-file-names=windows –random-wait "http://jra.jp/datafile/record/"```
