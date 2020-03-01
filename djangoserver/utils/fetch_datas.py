import os, sys, re, time
proj_path = "/Users/valentin/Documents/jkpg/Semester2/machine_learning/fake-news-predictor/djangoserver"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoserver.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.gis.views import feed

from fnp.models import *
import pandas as pd


def fetch_urls(url):
  return True


def parse_csv():
  data = panda.read_csv("../datasets/politifact_data.csv")
  print(data.head())


if __name__ == "__main__":
    parse_csv()
