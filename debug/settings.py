import os
from pathlib import Path
from dotenv import load_dotenv

envpath = Path(__file__).parent.parent.parent/'.env'
load_dotenv(envpath)
env = os.environ

DATABASE_URL = env.get('DATABASE_URL')
if DATABASE_URL.startswith('postgres://'): DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
ES_USERID = env.get('ES_USERID')
ES_PASSWORD = env.get('ES_PASSWORD')
ES_HOST = env.get('ES_HOST')
ES_PORT = env.get('ES_PORT')
ES_URL = env.get('ES_URL')
