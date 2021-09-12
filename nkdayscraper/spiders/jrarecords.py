# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import FormRequest
from nkdayscraper.items import JrarecordItem
import re
import datetime as dt

jst = dt.timezone(dt.timedelta(hours=9))

class JrarecordsSpider(CrawlSpider):
    name = 'jrarecords'
    allowed_domains = ['jra.jp']
    # start_urls = ['https://jra.jp/datafile/record/']

    rules = (
        Rule(
            LinkExtractor(
                allow=['jra.jp/JRADB'],
                deny=[
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
                # restrict_css = ['ul.link_list.multi.div5']
            ),
            follow=True
        ),
    )

    custom_settings = {
        'ITEM_PIPELINES': {'nkdayscraper.pipelines.JrarecordsscraperPipeline': 300}
    }

    def start_requests(self):
        yield FormRequest(
            url='https://jra.jp/JRADB/accessW.html',
            formdata={'cname': 'pr13rli00/8E'},
            # meta={'playwright': True, 'playwright_include_page': True},
            callback=self.parse_racecourse_url
        )

    # async
    def parse_racecourse_url(self, response):
        # page = response.meta['playwright_page']
        re_expr = re.compile("return doAction\('(.*?)', '(.*?)'\);")
        # a_list = await page.query_selector_all('ul.link_list.div5 > li > a')
        a_list = response.css('ul.link_list.div5 > li > a')
        for a in a_list:
            # onclick = await a.get_attribute('onclick')
            onclick = a.css('::attr(onclick)').get()
            match = re.match(re_expr, onclick)
            yield FormRequest(
                url='https://jra.jp/JRADB/accessW.html',
                formdata={'cname': match.groups()[1]},
                callback=self.parse_records
            )

        # await page.close()

    # async
    def parse_records(self, response):
        item = JrarecordItem()
        contentsBody = response.css('#contentsBody')
        item['place'] = re.sub(r'<h2>中央競馬レコードタイム　|競馬場</h2>', '', response.css('div.main h2').get())
        h3list = contentsBody.css('h3')
        headings = [[x for x in h3.css('span::text').getall() if not re.search(r'\n|\r\n|コース', x)] for h3 in h3list]
        tbodys = contentsBody.css('table.place tbody')
        for racetype in zip(headings, tbodys):
            item['coursetype'] = racetype[0][0]

            item['generation'] = racetype[0][1]
            for racerow in racetype[1].css('tr'):
                texts = [x for x in racerow.css('::text').getall() if not re.search(r'\n|\r\n|基準', x)]
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
                coursecondition = re.sub(r'[（）]', '', texts[11]).split('・');
                item['weather'] = coursecondition[0]
                item['coursecondition'] = coursecondition[1]
                item['reference'] = True if '基準' in racerow.css('::text').getall() else False

                for target in ['distance', 'age', 'distance']:
                    if item[target] is not None: item[target] = int(item[target])

                for target in ['jockeyweight']:
                    if item[target] is not None: item[target] = float(item[target])

                yield item
