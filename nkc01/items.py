# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Nkc01Item(scrapy.Item):
    raceid = scrapy.Field()
    place = scrapy.Field()
    racenum = scrapy.Field()
    title = scrapy.Field()
    cource = scrapy.Field()
    distance = scrapy.Field()
    cw_ccw = scrapy.Field()
    weather = scrapy.Field()
    condition = scrapy.Field()
    posttime = scrapy.Field()
    date = scrapy.Field()
    raceage = scrapy.Field()
    starters = scrapy.Field()
    addedmoneylist = scrapy.Field()

    placenum = scrapy.Field()
    postnum = scrapy.Field()
    horsenum = scrapy.Field()
    horsename = scrapy.Field()
    sex = scrapy.Field()
    age = scrapy.Field()
    weight = scrapy.Field()
    jockey = scrapy.Field()
    time = scrapy.Field()
    margin  = scrapy.Field()
    fav = scrapy.Field()
    odds = scrapy.Field()
    last3f = scrapy.Field()
    position = scrapy.Field()
    trainer = scrapy.Field()
    horseweight = scrapy.Field()
    horseweightdiff = scrapy.Field()
