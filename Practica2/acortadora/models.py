from django.db import models

# Create your models here.

class url(models.Model):
	original = models.CharField(max_length=256)
	acortada = models.CharField(max_length=256)
	def __str__(self):
		return self.original + ', ' + self.acortada	



