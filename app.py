# %%
from flask import Flask, render_template, jsonify#, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_session import flask_scoped_session
from scrapy.utils.project import get_project_settings
from nkdayscraper.models import HorseResult, Session
from nkdayscraper.spiders.nkday import NkdaySpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
from flask_cors import CORS
# from scrapy.crawler import CrawlerProcess

import argparse as argp
import subprocess as sp
import shlex as se
# import pandas as pd
import pathlib as pl
import uvicorn, os, sys, getpass, csv#, json

# pd.set_option('display.max_columns', 100);pd.set_option('display.max_rows', 500)
parser = argp.ArgumentParser()
parser.add_argument('-H', '--host', type=str, default='0.0.0.0')
parser.add_argument('-p', '--port', type=int, default=5000)
parser.add_argument('-l', '--log-level', type=str, default='info')
parser.add_argument('--orig', action='store_true')
parser.add_argument('--reload', action='store_true')
args = parser.parse_args()
print('args: ', args, '\n')

user = getpass.getuser()
versionmm = str(sys.version_info.major) + str(sys.version_info.minor)
pypath = 'C:\\Users\\' + user + '\\AppData\\Local\\Programs\\Python\\Python' + versionmm
env = os.environ
env['PYTHONPATH'] = ';'.join([
    os.getcwd(),
    pypath,
    pypath + '\\python' + versionmm + '.zip',
    pypath + '\\DLLs',
    pypath + '\\lib',
    pypath + '\\lib\\site-packages',
    pypath + '\\lib\\site-packages\\win32',
    pypath + '\\lib\\site-packages\\win32\\lib',
    pypath + '\\lib\\site-packages\\Pythonwin'
])

DATABASE_URL = get_project_settings().get('DATABASE_URL')

app = Flask(__name__) if args.orig else Flask(
    __name__,
    static_folder = './dist',
    template_folder = './dist'
)
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.variable_start_string = '{@'
app.jinja_env.variable_end_string = '@}'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)
session = flask_scoped_session(Session, app)
data = HorseResult.getRaceResults(session)
# for key, df in data.items(): df.to_pickle('data/pickle/' + key + '.pkl')
# data = {key: pd.read_pickle('data/pickle/' + key + '.pkl') for key in data.keys()}
# for key, df in data.items(): df.to_pickle('data/pickle/' + key + '.pkl')
data['racesdf'].to_json('data/json/raceresults.json', orient='table', force_ascii=False)
data['racesdf'].to_csv('data/csv/raceresults.csv', index=False, quoting=csv.QUOTE_ALL)
# jsonforapi = pl.Path('data/json/raceresults.json').read_text()

pass
# %%
# @app.route('/')
# def index():
#     return redirect(url_for('nkday'))

@app.route('/nkday/')
def nkday():
    return render_template('index.html', **data)

@app.route('/nkraces/')
def nkraces():
    return render_template('nkraces.vue', **data)

@app.route('/api/', methods=['GET', 'POST'])
def api():
    # return jsonforapi
    return data['json']

@app.route('/crawl', methods=['GET'])
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

@app.route('/crawlsp', methods=['GET'])
def crawlsp():
    cmd = 'pwsh -Command nkrun'
    p1 = sp.Popen(se.split(cmd), stderr=sp.PIPE, stdout=sp.PIPE, shell=True, env=env)
    data = {'p1': {'output': [x.decode('cp932') for x in p1.communicate()], 'status': p1.returncode}}
    return jsonify(data)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level, interface='wsgi', lifespan='off', reload=args.reload, workers=1)
