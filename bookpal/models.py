from django.db import models

class TodayBest(models.Model):
	date = models.CharField(max_length=10)
	genre = models.CharField(max_length=10)
	title = models.CharField(max_length=50)
	intro = models.TextField()

	def __str__(self): #I don't understand
		return self.title
