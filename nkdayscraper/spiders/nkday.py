# -*- coding: utf-8 -*-
import re, datetime as dt#, scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from nkdayscraper.items import HorseResultItem, PaybackItem, RaceItem
from nkdayscraper.utils.functions import getTargetDate
# from scrapy.shell import inspect_response

class NkdaySpider(CrawlSpider):
    name = 'nkday'
    allowed_domains = ['race.netkeiba.com']
    # start_urls = ['http://race.netkeiba.com/']

    rules = (
        Rule(
            LinkExtractor(
                allow = ['race.netkeiba.com'],
                deny = ['race.netkeiba.com/race/movie.html'],
                restrict_css = ['.RaceList_Data']
            ),
            callback = 'parse_races', follow = True
        ),
    )

    custom_settings = {
        'ITEM_PIPELINES': {'nkdayscraper.pipelines.NkdayscraperPipeline': 300}
    }

    def __init__(self, date=None, *args, **kwargs):
        super(NkdaySpider, self).__init__(*args, **kwargs)
        baseurl = 'https://race.netkeiba.com/top/race_list_sub.html?kaisai_date='
        if not date: date = f'{getTargetDate():%Y%m%d}'
        self.start_urls = [f'{baseurl}{date}']
        self.date = date

    def parse_races(self, response):
        raceinfo = response.css('#page')
        raceplaceurl = response.request.url
        raceid = raceplaceurl.split('race_id=')[1].split('&rf=')[0]

        item = RaceItem()
        item['raceid'] = raceid
        item['year'] = item['raceid'][0:4]
        racelist_namebox = raceinfo.css('.RaceList_NameBox')
        racedata02 = racelist_namebox.css('.RaceData02 span::text').getall()
        item['place'] = racedata02[1]
        item['holdtimesnum'] = racedata02[0].split('回')[0]
        item['holddaysnum'] = racedata02[2].split('日目')[0]
        item['racenum'] = racelist_namebox.css('.RaceList_Item01 .RaceNum::text').getall()[1].strip().split('R')[0]
        item['title'] = racelist_namebox.css('.RaceName::text').get().strip()
        coursetype = re.split('(\d+)|m', racelist_namebox.css('.RaceData01 span::text').get().strip())
        item['coursetype'] = {'芝': '芝', 'ダ': 'ダート', '障': '障害'}.get(coursetype[0])
        item['distance'] = coursetype[1]
        racedetail = racelist_namebox.css('.RaceData01::text')[1].get().strip()
        courseinfo = re.split('[()]', racedetail)
        item['courseinfo1'] = courseinfo[1][0]
        courseinfo3 = courseinfo[1][1:].split('\xa0')
        item['courseinfo2'] = (re.sub('[-周]', '', courseinfo3[0].strip()) or '') if item['courseinfo1'] != '直' else ''
        item['courseinfo3'] = courseinfo3[1] if len(courseinfo3) > 1 else None
        item['agecondition'] = racedata02[3]
        item['classcondition'] = racedata02[4]
        item['racecondition'] = racedata02[5] if racedata02[5:6] and racedata02[5].strip() else None
        item['weight'] = racedata02[6] if racedata02[6:7] else None
        conditions01 = courseinfo[2].split('天候:')
        item['weather'] = conditions01[1] if conditions01[1:2] else None
        conditions02 = raceinfo.css('.RaceData01 [class^="Item"]::text').get()
        item['coursecondition'] = conditions02.split('馬場:')[1] if conditions02 is not None else None
        raceyear = f"{item['year']}年"
        racedate = raceinfo.css('.RaceList_Date dd.Active a::text').get()
        if not racedate.endswith('日'): racedate = racedate.replace('/', '月') + '日'
        racetime = racelist_namebox.css('.RaceData01::text').get().strip().split('発走')[0]
        item['date'] = dt.datetime.strptime(f'{raceyear}{racedate}+09:00', '%Y年%m月%d日%z')
        item['datetime'] = dt.datetime.strptime(f'{raceyear}{racedate} {racetime}:00+09:00', '%Y年%m月%d日 %H:%M:%S%z') if racetime != '' else None
        item['posttime'] = dt.datetime.strptime(f'{racetime}+09:00', '%H:%M%z').timetz() if racetime != '' else None

        if(list(filter(lambda x: '歳' in x, racedata02)) != []):
            item['generation'] = '2歳' if int(racedata02[3].split('歳')[0][-1]) == 2 else '3歳以上'
        else:
            item['generation'] = None

        item['starters'] = racedata02[7].split('頭')[0]
        addedmoney_list = [int(x) * 1000 for x in racedata02[8].split('本賞金:')[1].split('万円')[0].split(',')]
        item['addedmoney_1st'] = addedmoney_list[0]
        item['addedmoney_2nd'] = addedmoney_list[1]
        item['addedmoney_3rd'] = addedmoney_list[2]
        item['addedmoney_4th'] = addedmoney_list[3]
        item['addedmoney_5th'] = addedmoney_list[4]
        item['requrl'] = response.request.url

        if item['coursetype'] == '障害':
            if item['courseinfo2'] == 'ダート':
                item['coursetype'] = 'ダート'
                item['courseinfo1'] = 'ダート'
            else:
                item['coursetype'] = item['courseinfo1']
                if item['place'] == '中山' and item['distance'] in ['3350', '4250'] and item['generation'] == '3歳以上' and item['courseinfo1'] == '芝' and item['courseinfo2'] == '外':
                    item['courseinfo1'] = '外'

            if item['courseinfo2'] == '外内': item['courseinfo1'] = '外内'
            item['courseinfo2'] = ''

            item['generation'] = '障害' + item['generation']

        for target in ['year', 'racenum', 'distance', 'starters']:
            if item[target] is not None: item[target] = int(item[target])

        yield item

        item = PaybackItem()
        result_pay_back = response.css('.Result_Pay_Back')
        paybacktbldiv = result_pay_back.css('.ResultPaybackLeftWrap .FullWrap')
        item['raceid'] = raceid
        for pooltype in ['tansho', 'fukusho', 'wakuren', 'umaren', 'wide', 'umatan', 'fuku3', 'tan3']:
            pooltr = paybacktbldiv.css('table tbody tr.' + pooltype.capitalize())
            item[pooltype] = [int(text) for text in pooltr.css('.Result ::text').getall() if '\n' not in text]
            item[f'{pooltype}pay'] = [int(text.rstrip('円').replace(',', '')) for text in pooltr.css('.Payout ::text').getall() if '\n' not in text]
            item[f'{pooltype}fav'] = [int(text.rstrip('人気').replace(',', '')) for text in pooltr.css('.Ninki ::text').getall() if '\n' not in text]

        yield item

        for tr in raceinfo.css('#All_Result_Table tbody tr'):
            item = HorseResultItem()
            horseurl = tr.css('.Horse_Info .Horse_Name a::attr(href)').get()
            item['raceid'] = raceid
            item['ranking'] = tr.css('td')[0].css('div::text').get().strip()
            item['postnum'] = tr.css('td')[1].css('div::text').get()
            item['horseid'] = horseurl.split('/')[-1]
            item['horsenum'] = tr.css('td')[2].css('div::text').get()
            item['horsename'] = tr.css('td')[3].css('.Horse_Name a::text').get()
            item['horseurl'] = horseurl
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
                racetime = tr.css('td')[7].css('.RaceTime::text').get()
                item['time'] = dt.datetime.strptime(racetime, '%M:%S.%f').time() if racetime is not None and item['ranking'] != '中止' else None
                margin = tr.css('td')[8].css('.RaceTime::text').get()
                item['margin'] = (margin if margin is not None else '0') if item['ranking'] != '中止' else item['ranking']
                item['fav'] = tr.css('td')[9].css('span::text').get()
                item['odds'] = tr.css('td')[10].css('span::text').get()
                last3f = tr.css('td')[11].css('::text').get().strip()
                item['last3f'] = last3f if last3f and item['ranking'] != '中止' else None
                passageratetext = tr.css('td')[12].css('::text').get().strip()
                item['passageratelist'] = [int(x) for x in passageratetext.split('-')] if passageratetext != '' else None
                item['passagerate_1st'] = item['passageratelist'][0] if item['passageratelist'] is not None and item['passageratelist'][0:1] else None
                item['passagerate_2nd'] = item['passageratelist'][1] if item['passageratelist'] is not None and item['passageratelist'][1:2] else None
                item['passagerate_3rd'] = item['passageratelist'][2] if item['passageratelist'] is not None and item['passageratelist'][2:3] else None
                item['passagerate_4th'] = item['passageratelist'][3] if item['passageratelist'] is not None and item['passageratelist'][3:4] else None
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

            for target in ['ranking', 'postnum', 'horsenum', 'age', 'fav']:
                if item[target] is not None: item[target] = int(item[target])

            for target in ['jockeyweight', 'odds', 'last3f', 'horseweight', 'horseweightdiff']:
                if item[target] is not None: item[target] = float(item[target])

            yield item
