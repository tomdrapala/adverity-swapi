from django.db import models
from django.contrib.postgres.fields import ArrayField


class People(models.Model):
    name = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='people')


class Character(models.Model):
    name = models.CharField(max_length=150)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    mass = models.PositiveSmallIntegerField(null=True, blank=True)
    birth_year = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    homeworld = models.CharField(max_length=100, null=True, blank=True)
    hair_color = ArrayField(base_field=models.CharField(max_length=50), null=True, blank=True, size=10)
    eye_color = ArrayField(base_field=models.CharField(max_length=50), null=True, blank=True, size=10)
    skin_color = ArrayField(base_field=models.CharField(max_length=50), null=True, blank=True, size=10)

    def __repr__(self):
        return f'Character object - {self.name}'
