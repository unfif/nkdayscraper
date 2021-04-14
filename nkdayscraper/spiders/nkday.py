# -*- coding: utf-8 -*-
import re, datetime as dt#, scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import HorseResultItem, PaybackItem, RaceItem
# from scrapy.shell import inspect_response

today = dt.date.today()
if today.weekday() in [5, 6]:
    targetdate = today
else:
    targetdate = today - dt.timedelta((today.weekday() + 1) % 7)

date = f'{targetdate:%Y%m%d}'
baseurl = 'https://race.netkeiba.com/top/race_list_sub.html?kaisai_date='

class NkdaySpider(CrawlSpider):
    name = 'nkday'
    allowed_domains = ['race.netkeiba.com', '127.0.0.1']
    # start_urls = ['http://race.netkeiba.com/']

    rules = (
        Rule(
            LinkExtractor(
                allow = ['race.netkeiba.com', '127.0.0.1'],
                deny = ['race.netkeiba.com/race/movie.html'],
                restrict_css = ['.RaceList_Data']
            ),
            callback = 'parse_races', follow = True
        ),
    )

    custom_settings = {
        'ITEM_PIPELINES': {'nkdayscraper.pipelines.NkdayscraperPipeline': 300}
    }

    def __init__(self, date=date, *args, **kwargs):
        super(NkdaySpider, self).__init__(*args, **kwargs)
        self.start_urls = [baseurl + date]

    # def start_requests(self):
    #     url = 'http://oldrace.netkeiba.com/?pid=race_list_sub&id=c' + cdate
    #     yield scrapy.Request(url, callback=self.parse_races)

    def parse_races(self, response):
        raceinfo = response.css('#page')
        raceplaceurl = response.request.url
        raceid = raceplaceurl.split('race_id=')[1].split('&rf=')[0]

        item = RaceItem()
        item['raceid'] = raceid
        item['year'] = item['raceid'][0:4]
        item['place'] = raceinfo.css('.RaceKaisaiWrap li.Active a::text').get()
        racelist_namebox = raceinfo.css('.RaceList_NameBox')
        item['racenum'] = racelist_namebox.css('.RaceList_Item01 .RaceNum::text').get().split('R')[0]
        item['title'] = racelist_namebox.css('.RaceName::text').get().strip()
        coursetype = re.split('(\d+)|m', racelist_namebox.css('.RaceData01 span::text').get().strip())
        item['coursetype'] = {'芝': '芝', 'ダ': 'ダート', '障': '障害'}.get(coursetype[0])
        item['distance'] = coursetype[1]
        racedetail = racelist_namebox.css('.RaceData01::text')[1].get().strip()
        courseinfo = re.split('[()]', racedetail)
        item['courseinfo1'] = courseinfo[1][0]
        item['courseinfo2'] = (courseinfo[1][1:].strip().replace('-', '') or '') if item['courseinfo1'] != '直' else ''

        item['weather'] = courseinfo[2].split('天候:')[1]
        item['condition'] = raceinfo.css('.RaceData01 [class^="Item"]::text').get().split('馬場:')[1]
        raceyear = item['year'] + '年'
        racedate = raceinfo.css('.RaceList_Date dd.Active a::text').get()
        if not racedate.endswith('日'): racedate = racedate.replace('/', '月') + '日'
        racetime = racelist_namebox.css('.RaceData01::text').get().strip().split('発走')[0]
        item['datetime'] = dt.datetime.strptime(raceyear + racedate + ' ' + racetime + ':00+09:00', '%Y年%m月%d日 %H:%M:%S%z')
        item['date'] = dt.datetime.strptime(raceyear + racedate + '+09:00', '%Y年%m月%d日%z')
        item['posttime'] = dt.datetime.strptime(racetime + '+09:00', '%H:%M%z').timetz()
        racedata02 = racelist_namebox.css('.RaceData02 span::text').getall()
        item['generation'] = '2歳' if int(racedata02[3].split('歳')[0][-1]) == 2 else '3歳以上'
        item['racegrade'] = racedata02[3:7]
        item['starters'] = racedata02[7].split('頭')[0]
        item['addedmoneylist'] = [int(x) * 1000 for x in racedata02[8].split('本賞金:')[1].split('万円')[0].split(',')]
        item['requrl'] = response.request.url

        if item['coursetype'] == '障害':
            if item['courseinfo2'] == 'ダート':
                item['coursetype'] = 'ダート'
                item['courseinfo1'] = 'ダート'
            else:
                item['coursetype'] = item['courseinfo1']
                # if item['courseinfo1'] == '芝': item['courseinfo1'] = item['courseinfo2']
                if item['place'] == '中山' and item['generation'] == '3歳以上' and item['distance'] == '3350' and item['courseinfo1'] == '芝' and item['courseinfo2'] == '外':
                    item['courseinfo1'] = '外'

            if item['courseinfo2'] == '外内': item['courseinfo1'] = '外内'
            item['courseinfo2'] = ''
                
            item['generation'] = '障害' + item['generation']

        yield item

        item = PaybackItem()
        result_pay_back = response.css('.Result_Pay_Back')
        paybacktbldiv = result_pay_back.css('.ResultPaybackLeftWrap .FullWrap')
        item['raceid'] = raceid
        for pooltype in ['tansho', 'fukusho', 'wakuren', 'umaren', 'wide', 'umatan', 'fuku3', 'tan3']:
            pooltr = paybacktbldiv.css('table tbody tr.' + pooltype.capitalize())
            item[pooltype] = [int(text) for text in pooltr.css('.Result ::text').getall() if text != '\n']
            item[pooltype + 'pay'] = [int(text.rstrip('円').replace(',', '')) for text in pooltr.css('.Payout ::text').getall() if text != '\n']
            item[pooltype + 'fav'] = [int(text.rstrip('人気').replace(',', '')) for text in pooltr.css('.Ninki ::text').getall() if text != '\n']

        yield item

        for tr in raceinfo.css('#All_Result_Table tbody tr'):
            item = HorseResultItem()
            item['raceid'] = raceid
            item['ranking'] = tr.css('td')[0].css('div::text').get().strip()
            item['postnum'] = tr.css('td')[1].css('div::text').get()
            item['horsenum'] = tr.css('td')[2].css('div::text').get()
            item['horsename'] = tr.css('td')[3].css('.Horse_Name a::text').get()
            item['horseurl'] = tr.css('.Horse_Info .Horse_Name a::attr(href)').get()
            horse_info_detail = tr.css('td')[4].css('.Horse_Info_Detail span::text').get().strip()
            item['sex'] = {'牡':'牡','牝':'牝','騙':'騙','せ':'騙','セ':'騙','せん':'騙','セン':'騙'}.get(horse_info_detail[0])
            item['age'] = int(horse_info_detail[1:])
            item['jockeyweight'] = tr.css('td')[5].css('.JockeyWeight::text').get()
            item['jockey'] = ''.join(tr.css('td')[6].css('a ::text').getall()).strip().lstrip('▲ △ ★ ☆ ◇')
            item['jockeyurl'] = tr.css('td')[6].css('a ::attr(href)').get()
            item['affiliate'] = tr.css('td')[13].css('span::text').get()
            item['trainer'] = tr.css('td')[13].css('a::text').get()
            item['trainerurl'] = tr.css('td')[13].css('a::attr(href)').get()

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
                item['horseweightdiff'] = re.split('[()+]', tr.css('td')[14].css('small::text').get() or '(-0)')[-2]
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

            # intkeys = []
            # itemkeys = list(item.keys())
            # for itemkey in itemkeys:
            #     if itemkey.endswith('num'): intkeys.append(itemkey)

            # intkeys.extend(['distance', 'starters', 'age', 'fav', 'horseweight', 'horseweightdiff'])
            # for intkey in intkeys:
            #     if item[intkey] is not None: item[intkey] = int(item[intkey])
            # for floatkey in ['jockeyweight', 'odds', 'last3f']:
            #     if item[floatkey] is not None: item[floatkey] = float(item[floatkey])

            yield item
