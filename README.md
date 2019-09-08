del results01.json; scrapy crawl nkday -a date=p0811 -o results01.json --nolog
rm results01.json & scrapy crawl nkday -a date=p0811 -o results01.json --nolog

flask run --debugger --reload
web: flask run --host=0.0.0.0 --port=$PORT

$env:PYTHONPATH = "."

twistd web --wsgi nkcflask01.app.app --listen=tcp:5000
web: wistd web --wsgi nkcflask01.app.app --listen=tcp:$PORT

________________________________________________________________________________
# results01.json for scrapy
del results01.json; scrapy crawl nkday -a date=c0907 -o results01.json --nolog

cat results01.json | jq -c '.[] | {"index": {"_index": "nkdayraces"}}, .' > es01.json

# es01.json for Elasticsearch
cat results01.json | sed -r 's/([0-9]{4})-([0-9]{2})-([0-9]{2})/\1\/\2\/\3/g' | jq -c '.[] | {"index": {"_index": "nkdayraces"}}, .' > es01.json

<!-- cat results01.json | jq -c '.[] | {"index": {"_index": "nkdayraces"}},.' | sed -z 's/\n/,\n/g' > es01.json -->

curl -XGET https://k2mq362g48:8jejkoxzm3@bonsign-7182717687.ap-southeast-2.bonsaisearch.net:443/_stats

curl -XPOST -H "Content-Type: application/x-ndjson" https://k2mq362g48:8jejkoxzm3@bonsign-7182717687.ap-southeast-2.bonsaisearch.net:443/_bulk --data-binary @es01.json

sudo date -s "08/29 20:59 2019"

mongoimport --db netkeiba --collection nkdayraces --file results02.json --jsonArray --drop

mongoimport --uri "mongodb+srv://undo5:marehito@mongui-t1cam.gcp.mongodb.net/netkeiba?retryWrites=true&w=majority" --collection nkdayraces --file results02.json --jsonArray --drop

<!-- cat results01.json | sed -r 's/"([0-9]{4}-[0-9]{2}-[0-9]{2}) ([0-9]{2}:[0-9]{2}:[0-9]{2})"/ISODate("\1T\2Z")/g' > results02.json -->

# results02.json for mongoDB
cat results01.json | sed -r 's/"([0-9]{4}-[0-9]{2}-[0-9]{2}) ([0-9]{2}:[0-9]{2}:[0-9]{2})"/{"\$date": "\1T\2.000+09:00"}/g' | sed -r 's/"([0-9]{4}-[0-9]{2}-[0-9]{2})"/{"\$date": "\1T00:00:00.000+09:00"}/g' > results02.json
