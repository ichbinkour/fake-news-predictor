import os, sys, re, time
proj_path = "/Users/valentin/Documents/jkpg/Semester2/machine_learning/fake-news-predictor/djangoserver"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoserver.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.gis.views import feed

from fnp.models import *
from fnp.modules.init_dictionary import *
import pandas as pd
from django.db.models import Count

import numpy as np

ed = EnDictionary()
ed.init()

def parse_csv():
    data = pd.read_csv("./datasets/politifact_data.csv", delimiter=";")
    matchurl = re.compile('.*.pdf')

    for index, row in data.iterrows():
        q_class = -1

        print('Attempting:', row['id'])
        if row['label'] == "FAKE":
            q_class = 1
        else:
            q_class = 0

        if not DictionaryEntry.objects.filter(news_id=row['id']).exists():
            if row['news_url'] != '' and not matchurl.match(row['news_url']):
                if ed.load_url(row['news_url'], q_class, row['id']):
                    print('Loaded OK:', row['id'])
            else:
                print("Wrong url format.")
        else:
            print("SKIPED: already in the database.")
        print("---------------------")
    print("DONE")
    return

def delete_pdf():
    dic = DictionaryEntry.objects.all()
    matchurl = re.compile('.*.pdf')
    for elem in dic:
        if matchurl.match(elem.url):
            DictionaryEntry.objects.filter(news_id=elem.news_id).delete()


if __name__ == "__main__":
    parse_csv()
