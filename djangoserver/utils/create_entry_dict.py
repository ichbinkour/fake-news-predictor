import os, sys, re, time
proj_path = "/Users/valentin/Documents/jkpg/Semester2/machine_learning/fake-news-predictor/djangoserver"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoserver.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import numpy as np
from fnp.models import *


def read_database(percentage):
    datas = DictionaryEntry.objects.all()
    size = len(datas)
    worddict = WordDictionary.objects.all()
    print("Opening database...")

    for word in datas:
        alreadyInside = False
        for elem in worddict:
            if not alreadyInside and elem.news_id == word.news_id:
                alreadyInside = True
                print(elem.news_id, "=> Already Inside")
                continue
            else:
                break

        if not alreadyInside:
            dictionary = dict()

            print("Collecting datas from", word.news_id)
            dictionary[word.news_id] = word.formatted
            try:
                cd = create_dict(dictionary)
                add_dict_database(cd)
            except:
                print("Error while reading database")
                print(dictionary)
                return False
        percentage = percentage + 1
        print("%.2f" % ((percentage * 100) / size), "%", sep="", end=" ")
    return True


def create_dict(datas):
    wordDictionary = dict()
    print("Creating dict...")

    for key in datas:
        print(key)
        words = datas[key].split(' ')
        dictElem = list()
        wordDictionary[key] = [words[0]]
        for index in range(0, len(words) - 1):
            if words[index] not in dictElem:
                dictElem.append(words[index])
        wordDictionary[key] = dictElem
    return wordDictionary


def add_dict_database(dictionary):
    for key in dictionary:
        for word in dictionary[key]:
            try:
                if not WordDictionary.objects.filter(word=word).exists():
                    wd = WordDictionary(word=word, news_id=key)
                    wd.save()
            except:
                print('Error while saving new word into WordDictionary')
                return False
    return True


def delete_dict_database():
    d = WordDictionary.objects.all()
    for elem in d:
        elem.delete()


