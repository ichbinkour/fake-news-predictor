from django.db import models


class Article(models.Model):
  url = models.TextField()
  body_text = models.TextField()
  label = models.IntegerField()

  def loadDict(self):
    formatted = Article.objects.all()


class WordDictionary(models.Model):
  word = models.TextField()

  def loadWordDictionary(self):
    return WordDictionary.objects.all()


class AnalizedArticle(models.Model):
  url = models.TextField()
  predicted_label = models.IntegerField()
  fake_p = models.FloatField()
  dodgy_p = models.FloatField()
  real_p = models.FloatField()