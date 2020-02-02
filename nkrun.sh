#!/bin/bash
rm results01.json & scrapy crawl nkday -a date=$1 -o results01.json
