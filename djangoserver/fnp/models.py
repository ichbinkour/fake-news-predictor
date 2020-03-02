from django.db import models

class News(models.Model):
  body_text = models.TextField()
  medbias_score = models.FloatField()
  medbias_class = models.IntegerField()
  q_score = models.FloatField()
  q_class = models.IntegerField()
  origin_url = models.TextField()
  origin_source = models.TextField()

class DictionaryEntry(models.Model):
  news_id = models.TextField()
  url = models.TextField()
  formatted = models.TextField()
  q_class = models.IntegerField()

  def loadDict(self):
    formatted = DictionaryEntry.objects.all()

class WordDictionary(models.Model):
  word = models.TextField()

  def loadWordDictionary(self):
    return WordDictionary.objects.all()