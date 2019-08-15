del results01.json; scrapy crawl nkday -a date=p0811 -o results01.json --nolog
rm results01.json & scrapy crawl nkday -a date=p0811 -o results01.json --nolog

flask run --debugger --reload
web: flask run --host=0.0.0.0 --port=$PORT

$env:PYTHONPATH = "."

twistd web --wsgi nkcflask01.app.app --listen=tcp:5000
web: wistd web --wsgi nkcflask01.app.app --listen=tcp:$PORT
