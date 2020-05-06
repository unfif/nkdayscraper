from flask import Flask, render_template, redirect, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_session import flask_scoped_session
from scrapy.utils.project import get_project_settings
from nkdayscraper.models import HorseResult, Session

import subprocess as sp
import shlex as se
import os, sys, getpass

import argparse as argp
import uvicorn

parser = argp.ArgumentParser()
parser.add_argument('-H', '--host', type=str, default='0.0.0.0')
parser.add_argument('-p', '--port', type=int, default=5000)
parser.add_argument('-l', '--log-level', type=str, default='info')
parser.add_argument('--reload', action='store_true')
args = parser.parse_args()

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

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
session = flask_scoped_session(Session, app)
data = HorseResult.getRaceResults(session)

@app.route('/')
def index():
    return redirect(url_for('raceResults'))

@app.route('/nkday/')
def raceResults():
    return render_template('index.html', **data)

@app.route('/app/')
def dummy():
    return '<h2>Here is "/app/".</h2>'

@app.route('/crawl', methods=['GET'])
def crawl():
    cmd = 'pwsh -Command nkrun'
    p1 = sp.Popen(se.split(cmd), stderr=sp.PIPE, stdout=sp.PIPE, shell=True, env=env)
    data = {'p1': {'output': [x.decode('cp932') for x in p1.communicate()], 'status': p1.returncode}}
    return jsonify(data)

if __name__ == '__main__':
    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level, interface='wsgi', lifespan='off', reload=args.reload, workers=1)
