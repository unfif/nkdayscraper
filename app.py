# %%
from flask import Flask, render_template, jsonify, send_from_directory#, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from scrapy.crawler import CrawlerRunner#, CrawlerProcess
# from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from nkdayscraper.models import HorseResult#, Base, engine
from nkdayscraper.spiders.nkday import NkdaySpider
from nkdayscraper.utils.functions import getTargetDate
from twisted.internet import reactor

from argparse import ArgumentParser
import subprocess as sp
import shlex as se

import requests as rq
import uvicorn, os, sys, platform, getpass#, csv
import datetime as dt
import logging

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)

# from pandas import set_option; set_option('display.max_columns', 100); set_option('display.max_rows', 500)

def getArgs():
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', type=str, default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, default=5000)
    parser.add_argument('-l', '--log-level', type=str, default='info')
    parser.add_argument('--orig', action='store_true')
    parser.add_argument('--reload', action='store_true')
    parser.add_argument('-z', '--zip', action='store_true')
    args = parser.parse_args(args=[])
    logging.info(f'{args=}')

    return args

args = getArgs()
env = os.environ
DATABASE_URL = get_project_settings().get('DATABASE_URL')

if platform.system() == 'Windows':
    user = getpass.getuser()
    pyVersion = f'{sys.version_info.major}{sys.version_info.minor}'
    pyPath = f'C:\\Users\\{user}\\AppData\\Local\\Programs\\Python\\Python{pyVersion}'
    env['PYTHONPATH'] = ';'.join([
        os.getcwd(),
        pyPath, f'{pyPath}\\python{pyVersion}.zip', f'{pyPath}\\DLLs', f'{pyPath}\\lib',
        f'{pyPath}\\lib\\site-packages', f'{pyPath}\\lib\\site-packages\\win32',
        f'{pyPath}\\lib\\site-packages\\win32\\lib', f'{pyPath}\\lib\\site-packages\\Pythonwin'
    ])

app = Flask(__name__) if args.orig else Flask(
    __name__, static_folder = 'dist', template_folder = 'dist'
)
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.variable_start_string = '{@'
app.jinja_env.variable_end_string = '@}'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)
# Base.metadata.create_all(engine)
# %%
horseResult = HorseResult()
date = getTargetDate()
data = horseResult.getRecords(date)

# data['records'].to_json('data/json/raceresults.json', orient='table', force_ascii=False)
# data['records'].to_csv('data/csv/raceresults.csv', index=False, quoting=csv.QUOTE_ALL)

# for key, df in data.items(): df.to_pickle(f'data/pickle/{key}.pkl')
# data = {key: pd.read_pickle(f'data/pickle/{key}.pkl') for key in data.keys()}
# for key, df in data.items(): df.to_pickle(f'data/pickle/{key}.pkl')
# jsonforapi = Path('data/json/raceresults.json').read_text()
# %%
if(args.zip):
    from nkdayscraper.utils.ziptools import ZipTools
    from pathlib import Path
    jsonDir = Path('data/json')
    zipTools = ZipTools()
    zipTools.zipEachFilesInDir(jsonDir)

# %%
@app.get('/')
def index():
    return render_template('index.html')
#     return redirect(url_for('nkday'))

@app.get('/nkday/')
def nkday():
    return render_template('index.html', **data)

# @app.get('/nkraces/')
# def nkraces():
#     return render_template('nkraces.vue', **data)

# @app.get('/api/')
# def api():
#     # return jsonforapi
#     return data['json']

@app.get('/api/')
def getall():
    return data['json']

@app.get('/api/<string:date>/')
def api(date):
    date = dt.date(*[int(str) for str in date.split('-')])
    data = horseResult.getRecords(date)
    return data['json']

# @app.get('/api/<string:key>/')
# def api(key):
#     return data['json'][key]

@app.get('/crawl')
def crawl():
    # process = CrawlerProcess(get_project_settings())
    # process.crawl(NkdaySpider)
    # process.start()
    # runner = CrawlerRunner(get_project_settings())
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()
    d = runner.crawl(NkdaySpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    return jsonify({"status": True})

@app.get('/crawlsp')
def crawlsp():
    cmd = 'pwsh -Command nkrun'
    p1 = sp.Popen(se.split(cmd), stderr=sp.PIPE, stdout=sp.PIPE, shell=True, env=env)
    data = {'p1': {'output': [x.decode('cp932') for x in p1.communicate()], 'status': p1.returncode}}
    return jsonify(data)

@app.get('/nkdb/<string:dbtype>/<string:dbid>')
def get_nkdb(dbtype, dbid):
    response = rq.get(f'https://db.netkeiba.com/{dbtype}/{dbid}')
    response.encoding = response.apparent_encoding
    return response.text

@app.get('/nkrace/<string:raceid>')
def get_nkrace(raceid):
    response = rq.get(f'https://race.netkeiba.com/race/result.html?race_id={raceid}&rf=race_list')
    response.encoding = response.apparent_encoding
    return response.text

@app.get('/pedigree/<string:horseid>')
def get_nkpedigree(horseid):
    response = rq.get(f'https://db.netkeiba.com/horse/ped/{horseid}/')
    response.encoding = response.apparent_encoding
    return response.text

@app.get('/redirect/<string:url>')
def get_response(url):
    response = rq.get(url)
    response.encoding = response.apparent_encoding
    return response.text

@app.get('/', defaults={'path': ''})
@app.get('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.get('/now')
def get_now():
    return dt.datetime.now().isoformat()

@app.get('/assets/<path:filename>')
def get_asset(filename):
    return send_from_directory('./dist/assets/', filename)

# %%
if __name__ == '__main__':
    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level, interface='wsgi', lifespan='off', reload=args.reload, workers=1)

# %%
