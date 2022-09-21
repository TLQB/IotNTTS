from django.db import models

# Create your models here.


class IotNTTSData(models.Model):
	thoi_gian = models.CharField(max_length = 100)
	nhiet_do = models.IntegerField()
	ph  = models.IntegerField()
	oxy = models.IntegerField()

	def __str__(self):
		return self.thoi_gian 

class WarningData(models.Model):
	thoi_gian = models.CharField(max_length = 100)
	nhiet_do = models.IntegerField()
	ph  = models.IntegerField()
	oxy = models.IntegerField()

	def __str__(self):
		return self.thoi_gian 