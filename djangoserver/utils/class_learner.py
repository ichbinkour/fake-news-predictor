import os, sys, re, time
from sklearn.neural_network import *
from sklearn.model_selection import *
from sklearn.metrics import *
from sklearn.svm import *
import pickle

proj_path = "/Users/valentin/Documents/jkpg/Semester2/machine_learning/fake-news-predictor/djangoserver"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoserver.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from dict_builder import loadDict, loadExampleFromDatabase
from fnp.models import *


print("Setting up..")
cDict = loadDict()
qs_Examples = Article.objects.filter(label__lt=4)

print(qs_Examples.count())

print("Processing examples")
(Y_vector, examplesMatrix) = loadExampleFromDatabase(qs_Examples, cDict)

X_train, X_test, y_train, y_test = train_test_split(examplesMatrix, Y_vector, test_size=0.2)


chosen_models = {}

chosen_models['fnp/MLPC_model.sav'] = MLPClassifier(hidden_layer_sizes=(128,64,32,16,8), max_iter=2500)

for fname, model in chosen_models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print("Classification report: ")
    print(classification_report(predictions, y_test))
    print("***************")
    dosave = input("Save " + fname + "? ")
    if (dosave == 'y' or dosave == 'Y'):
        print("Saving...")
        pickle.dump(model, open(fname, 'wb'))
        print("Saved!")
    else:
        print("Not saved!")