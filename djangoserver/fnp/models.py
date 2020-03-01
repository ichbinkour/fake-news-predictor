from django.db import models

class News(models.Model):
  body_text = models.TextField()
  medbias_score = models.FloatField()
  medbias_class = models.IntegerField()
  q_score = models.FloatField()
  q_class = models.IntegerField()
  origin_url = models.TextField()
  origin_source = models.TextField()
