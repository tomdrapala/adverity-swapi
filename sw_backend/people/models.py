from django.db import models
from django.contrib.postgres.fields import ArrayField


class People(models.Model):
    class PeopleManager(models.Manager):
        # `is_removed` is not used right now, but we could use it in future to make sure our data is valid,
        # by setting up some logic for checking are all files still present in the file system.
        # Objects with non-existent files could be marked as removed, 
        # allowing us keep info that such file was created.
        # For example it could be some scheduled Celery task,
        # pos_save signal, function triggered by GET or POST signals etc.
        def existing(self):
            return self.filter(is_removed=False)

    objects = PeopleManager()

    file_name = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False, blank=True)



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
