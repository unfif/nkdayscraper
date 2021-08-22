# -*- coding: utf-8 -*-
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from nkdayscraper.items import JrarecordItem
import datetime as dt

jst = dt.timezone(dt.timedelta(hours=9))

class JrarecordSpider(CrawlSpider):
    name = 'jrarecords'
    allowed_domains = ['jra.jp']
    start_urls = ['https://jra.jp/datafile/record/']

    rules = (
        Rule(
            LinkExtractor(
                allow = ['jra.jp/datafile/record', '127.0.0.1'],
                deny = [
                    # 'https://jra.jp/datafile/record/sapporo.html',
                    # 'https://jra.jp/datafile/record/hakodate.html',
                    # 'https://jra.jp/datafile/record/fukushima.html',
                    # 'https://jra.jp/datafile/record/niigata.html',
                    # 'https://jra.jp/datafile/record/nakayama.html',
                    # 'https://jra.jp/datafile/record/tokyo.html',
                    # 'https://jra.jp/datafile/record/chukyo.html',
                    # 'https://jra.jp/datafile/record/kyoto.html',
                    # 'https://jra.jp/datafile/record/hanshin.html',
                    # 'https://jra.jp/datafile/record/kokura.html'
                ],
                restrict_css = ['ul.link_list.multi.div5']
            ),
            callback = 'parse_records', follow = True
        ),
    )

    custom_settings = {
        'ITEM_PIPELINES': {'nkdayscraper.pipelines.JrarecordsscraperPipeline': 300}
    }

    def parse_records(self, response):
        item = JrarecordItem()
        contentsBody = response.css('#contentsBody')
        item['place'] = response.css('#contents .content li.current a::text').get().split('競馬場')[0]
        h3list = contentsBody.css('h3')
        headings = [[x for x in h3.css('span::text').getall() if x not in ['\n', '\r\n', 'コース']] for h3 in h3list]
        tbodys = contentsBody.css('table.place tbody')
        for racetype in zip(headings, tbodys):
            item['coursetype'] = racetype[0][0]

            item['generation'] = racetype[0][1]
            for racerow in racetype[1].css('tr'):
                texts = [x for x in racerow.css('::text').getall() if x not in ['\n', '\r\n', '基準']]
                item['distance'] = texts[0].replace(',', '')
                courseinfo = texts[1].split('・')

                item['courseinfo1'] = courseinfo[0]
                item['courseinfo2'] = courseinfo[1] if len(courseinfo) > 1 else ''

                item['time'] = dt.datetime.strptime(('00:0' if ':' in texts[2] else '00:00:') + texts[2], '%H:%M:%S.%f').time()
                item['horsename'] = texts[3]
                item['sire'] = texts[4].split('：')[1]
                item['dam'] = texts[5].split('：')[1]
                item['sex'] = {'牡':'牡','牝':'牝','騙':'騙','せ':'騙','セ':'騙','せん':'騙','セン':'騙'}.get(re.split(r'\d+$', texts[6])[0])
                item['age'] = re.split(r'^[牡牝騙]|^せん', texts[6])[1]
                item['jockeyweight'] = texts[7]
                item['jockey'] = texts[8].split('\u3000')[0]
                item['jockeyfullname'] = texts[8].replace('\u3000', '')
                item['date'] = dt.date(int(texts[9].split('年')[0]), int(texts[10].split('月')[0]), int(re.split(r'[月日]', texts[10])[1]))
                condition = re.sub(r'[（）]', '', texts[11]).split('・');
                item['weather'] = condition[0]
                item['condition'] = condition[1]
                item['reference'] = True if '基準' in racerow.css('::text').getall() else False

                for target in ['distance', 'age', 'distance']:
                    if item[target] is not None: item[target] = int(item[target])

                for target in ['jockeyweight']:
                    if item[target] is not None: item[target] = float(item[target])

                yield item
