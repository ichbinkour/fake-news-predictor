import os, sys, re, time

proj_path = "/Users/valentin/Documents/jkpg/Semester2/machine_learning/fake-news-predictor/djangoserver"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoserver.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from fnp.modules.init_dictionary import FetchData
import pickle
from bs4 import BeautifulSoup
from .dict_builder import loadDict, loadExampleFromDatabase, buildExampleRow


def find_fnp(url):
    print("Loading models....")
    mlp_model = pickle.load(open('utils/MLPC_model.sav', 'rb'))

    print("Brain load successful.")

    print("Initializing dictionaries...")
    cDict = loadDict()
    ss = FetchData()
    ss.init()

    print("Attempting URL: " + url)
    if (ss.load_real_url(url)):
        articleX = buildExampleRow(ss.extractedText, cDict)
    else:
        print("Error on URL, exiting")
        exit(0)

    articleX = articleX.reshape(1, -1)

    mlp_prediction = mlp_model.predict(articleX)
    mlp_probabilities = mlp_model.predict_proba(articleX)

    return mlp_prediction, mlp_probabilities, url