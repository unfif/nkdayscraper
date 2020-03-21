# -*- coding: utf-8 -*-
import scrapy, re, requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from nkdayscraper.items import NkdayscraperItem
import datetime as dt

today = dt.date.today()
if today.weekday() in [5, 6]:
    targetdate = today
else:
    targetdate = today - dt.timedelta((today.weekday() + 1) % 7)

date = '{0:%Y%m%d}'.format(targetdate)

baseurl = 'https://race.netkeiba.com/top/race_list_sub.html?kaisai_date='

class NkdaySpider(CrawlSpider):
    name = 'nkday'
    allowed_domains = ['race.netkeiba.com', '127.0.0.1']
    # start_urls = ['http://race.netkeiba.com/']

    rules = (
        Rule(LinkExtractor(
            allow = ['race.netkeiba.com', '127.0.0.1'],
            deny = ['race.netkeiba.com/race/movie.html'],
            restrict_css = ['.RaceList_Data']
        ),
            callback = 'parse_races', follow = True
        ),
    )

    def __init__(self, date=date, *args, **kwargs):
        super(NkdaySpider, self).__init__(*args, **kwargs)
        self.start_urls = [baseurl + date]#'http://127.0.0.1:5555']

    # def start_requests(self):
    #     url = 'http://oldrace.netkeiba.com/?pid=race_list_sub&id=c' + cdate
    #     yield scrapy.Request(url, callback=self.parse_races)

    def parse_races(self, response):
        item = NkdayscraperItem()

        raceinfo = response.css('#page')
        raceplaceurl = response.request.url
        item['raceid'] = raceplaceurl.split('race_id=')[1].split('&rf=')[0]
        item['year'] = item['raceid'][0:4]
        item['place'] = raceinfo.css('.RaceKaisaiWrap li.Active a::text').get()
        RaceList_NameBox = raceinfo.css('.RaceList_NameBox')
        item['racenum'] = RaceList_NameBox.css('.RaceList_Item01 .RaceNum::text').get().split('R')[0]
        item['title'] = RaceList_NameBox.css('.RaceName::text').get().strip()
        courcetype = re.split('(\d+)|m', RaceList_NameBox.css('.RaceData01 span::text').get().strip())
        item['courcetype'] = courcetype[0]
        item['distance'] = courcetype[1]
        racecondition = RaceList_NameBox.css('.RaceData01::text')[1].get().strip()
        item['direction'] = re.split('[()]', racecondition)[1]
        item['weather'] = re.split('[()]', racecondition)[2].split('天候:')[1]
        item['condition'] = raceinfo.css('.RaceData01 [class^="Item"]::text').get().split('馬場:')[1]
        raceyear = item['year'] + '年'
        racedate = raceinfo.css('.RaceList_Date dd.Active a::text').get()
        if not racedate.endswith('日'): racedate = racedate.replace('/', '月') + '日'
        racetime = RaceList_NameBox.css('.RaceData01::text').get().strip().split('発走')[0]
        item['datetime'] = dt.datetime.strptime(raceyear + racedate + ' ' + racetime + ':00+09:00', '%Y年%m月%d日 %H:%M:%S%z')
        item['day'] = dt.datetime.strptime(raceyear + racedate + '+09:00', '%Y年%m月%d日%z')
        item['posttime'] = dt.datetime.strptime(racetime + '+09:00', '%H:%M%z').timetz()
        RaceData02 = RaceList_NameBox.css('.RaceData02 span::text').getall()
        item['racegrade'] = ','.join(RaceData02[3:7])
        item['starters'] = RaceData02[7].split('頭')[0]
        item['addedmoneylist'] = [int(x) * 1000 for x in RaceData02[8].split('本賞金:')[1].split('万円')[0].split(',')]

        for tr in raceinfo.css('#All_Result_Table tbody tr'):
            item['ranking'] = tr.css('td')[0].css('div::text').get().strip()
            item['postnum'] = tr.css('td')[1].css('div::text').get()
            item['horsenum'] = tr.css('td')[2].css('div::text').get()
            item['horsename'] = tr.css('td')[3].css('.Horse_Name a::text').get()
            Horse_Info_Detail = tr.css('td')[4].css('.Horse_Info_Detail .Detail_Left::text').get().strip()
            item['sex'] = Horse_Info_Detail[0]
            item['age'] = Horse_Info_Detail[1:]
            item['jockeyweight'] = tr.css('td')[5].css('.JockeyWeight::text').get()
            item['jockey'] = tr.css('td')[6].css('a::text').get().strip().lstrip('▲ △ ★ ☆ ◇')
            item['affiliate'] = tr.css('td')[13].css('span::text').get()
            item['trainer'] = tr.css('td')[13].css('a::text').get()

            if item['ranking'] not in ['取消', '除外']:
                item['time'] = dt.datetime.strptime(tr.css('td')[7].css('.RaceTime::text').get(), '%M:%S.%f').time() if item['ranking'] != '中止' else None
                margin = tr.css('td')[8].css('.RaceTime::text').get()
                item['margin'] = (margin if margin is not None else '0') if item['ranking'] != '中止' else item['ranking']
                item['fav'] = tr.css('td')[9].css('span::text').get()
                item['odds'] = tr.css('td')[10].css('span::text').get()
                last3f = tr.css('td')[11].css('::text').get().strip()
                item['last3f'] = last3f if last3f and item['ranking'] != '中止' else None
                passageratetext = tr.css('td')[12].css('::text').get().strip()
                item['passageratelist'] = [int(x) for x in passageratetext.split('-')] if passageratetext != '' else None
                item['horseweight'] = tr.css('td')[14].css('::text').get().strip()
                item['horseweightdiff'] = re.split('[()+]', tr.css('td')[14].css('small::text').get())[-2]
            else:
                item['time'] = None
                item['margin'] = item['ranking']
                item['fav'] = None
                item['odds'] = None
                item['last3f'] = None
                item['passageratelist'] = None
                item['horseweight'] = None
                item['horseweightdiff'] = None

            if item['ranking'] in ['中止', '取消', '除外']: item['ranking'] = None

            item['requrl'] = response.request.url

            intkeys = []
            itemkeys = list(item.keys())
            for itemkey in itemkeys:
                if itemkey.endswith('num'): intkeys.append(itemkey)

            intkeys.extend(['distance', 'starters', 'age', 'fav', 'horseweight', 'horseweightdiff'])
            for intkey in intkeys:
                if item[intkey] is not None: item[intkey] = int(item[intkey])
            for floatkey in ['jockeyweight', 'odds', 'last3f']:
                if item[floatkey] is not None: item[floatkey] = float(item[floatkey])

            yield item
