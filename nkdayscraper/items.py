# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from nkdayscraper.models import Race, Payback, Jrarecord, HorseResult

class RaceItem(scrapy.Item):
    model = Race
    raceid = scrapy.Field()

    year = scrapy.Field()
    place = scrapy.Field()
    holdtimesnum = scrapy.Field()
    holddaysnum = scrapy.Field()
    racenum = scrapy.Field()
    title = scrapy.Field()
    coursetype = scrapy.Field()
    distance = scrapy.Field()
    courseinfo1 = scrapy.Field()
    courseinfo2 = scrapy.Field()
    agecondition = scrapy.Field()
    classcondition = scrapy.Field()
    racecondition = scrapy.Field()
    weight = scrapy.Field()
    weather = scrapy.Field()
    coursecondition = scrapy.Field()
    datetime = scrapy.Field()
    date = scrapy.Field()
    posttime = scrapy.Field()
    generation = scrapy.Field()
    starters = scrapy.Field()
    addedmoney_1st = scrapy.Field()
    addedmoney_2nd = scrapy.Field()
    addedmoney_3rd = scrapy.Field()
    addedmoney_4th = scrapy.Field()
    addedmoney_5th = scrapy.Field()
    requrl = scrapy.Field()

class PaybackItem(scrapy.Item):
    model = Payback
    raceid = scrapy.Field()

    tansho = scrapy.Field()
    tanshopay = scrapy.Field()
    tanshofav = scrapy.Field()
    fukusho = scrapy.Field()
    fukushopay = scrapy.Field()
    fukushofav = scrapy.Field()
    wakuren = scrapy.Field()
    wakurenpay = scrapy.Field()
    wakurenfav = scrapy.Field()
    umaren = scrapy.Field()
    umarenpay = scrapy.Field()
    umarenfav = scrapy.Field()
    wide = scrapy.Field()
    widepay = scrapy.Field()
    widefav = scrapy.Field()
    umatan = scrapy.Field()
    umatanpay = scrapy.Field()
    umatanfav = scrapy.Field()
    fuku3 = scrapy.Field()
    fuku3pay = scrapy.Field()
    fuku3fav = scrapy.Field()
    tan3 = scrapy.Field()
    tan3pay = scrapy.Field()
    tan3fav = scrapy.Field()

class HorseResultItem(scrapy.Item):
    model = HorseResult
    raceid = scrapy.Field()

    ranking = scrapy.Field()
    postnum = scrapy.Field()
    horseid = scrapy.Field()
    horsenum = scrapy.Field()
    horsename = scrapy.Field()
    horseurl = scrapy.Field()
    sex = scrapy.Field()
    age = scrapy.Field()
    jockeyweight = scrapy.Field()
    jockey = scrapy.Field()
    jockeyurl = scrapy.Field()
    time = scrapy.Field()
    margin  = scrapy.Field()
    fav = scrapy.Field()
    odds = scrapy.Field()
    last3f = scrapy.Field()
    passageratelist = scrapy.Field()
    passagerate_1st = scrapy.Field()
    passagerate_2nd = scrapy.Field()
    passagerate_3rd = scrapy.Field()
    passagerate_4th = scrapy.Field()
    affiliate = scrapy.Field()
    trainer = scrapy.Field()
    trainerurl = scrapy.Field()
    horseweight = scrapy.Field()
    horseweightdiff = scrapy.Field()

class JrarecordItem(scrapy.Item):
    model = Jrarecord

    place = scrapy.Field()
    coursetype = scrapy.Field()
    generation = scrapy.Field()
    distance = scrapy.Field()
    courseinfo1 = scrapy.Field()
    courseinfo2 = scrapy.Field()
    time = scrapy.Field()
    horsename = scrapy.Field()
    sire = scrapy.Field()
    dam = scrapy.Field()
    sex = scrapy.Field()
    age = scrapy.Field()
    jockeyweight = scrapy.Field()
    jockey = scrapy.Field()
    jockeyfullname = scrapy.Field()
    date = scrapy.Field()
    weather = scrapy.Field()
    coursecondition = scrapy.Field()
    reference = scrapy.Field()
