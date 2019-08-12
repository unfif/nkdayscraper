del results01.json; scrapy crawl nktheday -a date=p0811 -o results01.json --nolog

rm results01.json & scrapy crawl nktheday -a date=p0811 -o results01.json --nolog

flask run --debugger --reload
