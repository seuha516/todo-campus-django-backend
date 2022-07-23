from django.db import models

# Create your models here.
class Calendar(models.Model):
    num=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=12)
    name=models.CharField(max_length=30)
    color=models.CharField(max_length=10)
    content=models.CharField(max_length=255)
    location=models.CharField(max_length=30)
    start=models.DateTimeField()
    end=models.DateTimeField()

    class Meta:
        db_table="calendar"