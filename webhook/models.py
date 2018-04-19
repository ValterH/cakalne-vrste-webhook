from django.db import models

class Procedure(models.Model):
    name = models.CharField(max_length=500)
    procedure_id = models.CharField(max_length=10)

class Region(models.Model):
    name = models.CharField(max_length=50)
    region_id = models.CharField(max_length=10)

class Urgency(models.Model):
    name = models.CharField(max_length=50)
    urgency_id = models.CharField(max_length=10)

class Group(models.Model):
	name = models.CharField(max_length=50)
	procedures = models.ManyToManyField(Procedure, verbose_name="list of procedures", blank=True)