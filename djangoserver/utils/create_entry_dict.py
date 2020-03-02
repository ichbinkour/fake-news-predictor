import os, sys, re, time
proj_path = "/Users/valentin/Documents/jkpg/Semester2/machine_learning/fake-news-predictor/djangoserver"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoserver.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from fnp.models import *


def read_database():
    dictionary = dict()
    datas = DictionaryEntry.objects.all()[:2]

    for cell in datas:
        if cell.news_id not in dictionary:
            dictionary[cell.news_id] = cell.formatted
    return dictionary


def create_dict(datas):
    wordDictionary = list()

    for key in datas:
        words = datas[key].split(' ')
        for word in words:
            if word not in wordDictionary:
                wordDictionary.append(word)
    return wordDictionary


def add_dict_database(dictionary):
    for word in dictionary:
        try:
            if not WordDictionary.objects.filter(word=word).exists():
                wd = WordDictionary(word=word)
                wd.save()
                print('Correctly added new word')
            else:
                print(word, "already exist in database")
        except:
            print('Error while saving new word into WordDictionary')
            return False

    return True


if __name__ == '__main__':
    datas = read_database()
    dictionary = create_dict(datas)
    add_dict_database(dictionary)
