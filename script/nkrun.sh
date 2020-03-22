#!/bin/bash
rm data/results01.json & scrapy crawl nkday -a date=$1 -o data/results01.json
