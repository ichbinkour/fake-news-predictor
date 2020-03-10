import os, sys, re, time
proj_path = "/Users/valentin/Documents/jkpg/Semester2/machine_learning/fake-news-predictor/djangoserver"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoserver.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from fnp.models import *
import numpy as np


def loadExampleFromDatabase(qs_ex, cDict):
    Y_vector = np.zeros(qs_ex.count(), dtype=np.int8)
    Y_vector_count = 0
    exampleMatrix = None

    for ex in qs_ex:
        Y_vector[Y_vector_count] = int(ex.label)
        Y_vector_count+=1
        if exampleMatrix is None:
            exampleMatrix = buildExampleRow(ex.body_text, cDict)
        else:
            exampleMatrix = np.vstack([exampleMatrix, buildExampleRow(ex.body_text, cDict)])
            print('.', Y_vector_count, end='', flush=True)

    return Y_vector, exampleMatrix



def loadDict():
    print('Getting word dictionary...')
    canonDict = WordDictionary.objects.all()
    cDict = {}
    for cw in canonDict:
        cDict[cw.word] = cw.pk

    return cDict


def buildExampleRow(body_text, cDict):
    dictSize = len(cDict.keys())
    one_ex_vector = np.zeros(dictSize + 2)
    cwords = body_text.split()

    for word in cwords:
        if word in cDict.keys():
            one_ex_vector[cDict[word] - 1] = 1
        else:
            print("This word does not exist in dictionary:", word)
    return one_ex_vector


def buildDict():
    qs_Examples = Article.objects.all()
    print("Examples: " + str(qs_Examples.count()))

    cDict = loadDict()

    for ex in qs_Examples:
        words = ex.body_text.split()
        for word in words:
            if word in cDict.keys():
                print('.', end="", flush=True)
            else:
                print('X', end="", flush=True)
                wd = WordDictionary(word=word)
                wd.save()
                cDict[word] = wd.pk


if __name__ == '__main__':
    buildDict()