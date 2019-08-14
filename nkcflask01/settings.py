import os
import pathlib as pl
from dotenv import load_dotenv

envpath = (pl.Path(__file__).parent.parent / '.env').resolve()
load_dotenv(envpath)
env = os.environ
