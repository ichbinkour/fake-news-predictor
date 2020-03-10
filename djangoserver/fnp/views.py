import os, sys, re, time

proj_path = "/Users/valentin/Documents/jkpg/Semester2/machine_learning/fake-news-predictor/djangoserver"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoserver.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Create your views here.
from fnp.models import Article, AnalizedArticle
from fnp.forms import AnalyzeUrlForm

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView

from utils.find_news_prediction import find_fnp

class Index(TemplateView):
    template_name = "index/index.html"

    def get(self, request):
        form = AnalyzeUrlForm()
        return render(request, self.template_name, {'form': form})


class Result(View):
    template_name = "result.html"

    def get(self):
        print("GET SAMER")

    def post(self, request):
        form = AnalyzeUrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            if not AnalizedArticle.objects.filter(url=url).exists():
                try:
                    print("Fetching url....")
                    ananylzed = find_fnp(url)
                    try:
                        al = AnalizedArticle(url=ananylzed[2], predicted_label=ananylzed[0][0], fake_p=ananylzed[1][0][1], dodgy_p=ananylzed[1][0][2], real_p=ananylzed[1][0][3])
                        al.save()
                        analyzed = AnalizedArticle.objects.filter(url=url)
                    except:
                        print("ERROR while saving database")
                except:
                    print("ERROR WHILE FETCHING")
                    return render(request, "index/index.html", {'error': "Error on HTTP request"})
            else:
                print("Already exist")
                analyzed = AnalizedArticle.objects.filter(url=url)
                args = {'form': form, 'url': url, 'data': analyzed}
                return render(request, self.template_name, args)

        args = {'form': form, 'url': url, 'data': analyzed}
        return render(request, self.template_name, args)


def post_url(request):
    if request.method == 'POST':

        form = AnalyzeUrlForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['url']
            if not AnalizedArticle.objects.filter(url=url).exists():
                try:
                    print("Fetching url....")
                    ananylzed = find_fnp(url)
                    try:
                        al = AnalizedArticle(url=ananylzed[2], predicted_label=ananylzed[0][0], fake_p=ananylzed[1][0][1], dodgy_p=ananylzed[1][0][2], real_p=ananylzed[1][0][3])
                        al.save()
                        analyzed = al
                    except:
                        print("ERROR while saving database")
                except:
                    print("ERROR WHILE FETCHING")
            else:
                analyzed = AnalizedArticle.objects.filter(url=url)
                return redirect('/result/')
    else:
        form = AnalyzeUrlForm()

    return render(request, 'result.html', {'form': form})
