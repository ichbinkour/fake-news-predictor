import os, sys, re, time

proj_path = "/Users/valentin/Documents/jkpg/Semester2/machine_learning/fake-news-predictor/djangoserver"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoserver.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.gis.views import feed

from fnp.models import Article
from fnp.modules.init_dictionary import *
import pandas as pd

import numpy as np

fetchd = FetchData()
fetchd.init()


def loadArticle():
    print("Getting article list...")
    article = Article.objects.all()
    cDict = {}

    for elem in article:
        cDict[elem.url] = elem.pk

    return cDict


def fetch_politifact_data():
    print("Reading dataset...")
    data = pd.read_csv("./datasets/politifact_data.csv", delimiter=";")
    notmatchurl = re.compile('.*.pdf')
    total_rows = len(data.index)

    article = loadArticle()

    for index, row in data.iterrows():
        print('Attempting:', row['id'])
        url = row['news_url']
        print(index+1, "/", total_rows, end="")
        print("")

        q_class = -1
        if row['label'] == "FAKE":
            q_class = 1
        else:
            q_class = 3

        if url in article:
            print("SKIPPED", row['id'])
        else:
            if url != '' and not notmatchurl.match(url):
                if fetchd.load_url(url, q_class):
                    print('Loaded OK:', row['id'])
                else:
                    print("Wrong url format.")
                time.sleep(1)
        print("---------")
    return


def fetch_mediachart_data():
    data = pd.read_csv("./datasets/adfontsmedia.csv", delimiter=",")
    notmatchurl = re.compile('.*.pdf')
    total_rows = len(data.index)

    for index, row in data.iterrows():
        q_class = row['Quality']
        label = -1
        url = row['Url']

        print(index, "/", total_rows, end="")
        print("")

        # FAKE
        if q_class <= 24:
            label = 1
        # DODGY
        elif q_class <= 32:
            label = 2
        # REAL
        elif q_class >= 33:
            label = 3

        if not Article.objects.filter(url=url).exists():
            if not notmatchurl.match(url):
                if fetchd.load_url(url, label):
                    print('Loaded OK')
            else:
                print("Wrong url format.")
            time.sleep(1)
        else:
            print("SKIPPED: already in the database.")
        print("DONE")
        print("---------------------")

    return


if __name__ == "__main__":
    fetch_politifact_data()
