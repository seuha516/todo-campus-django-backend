from django.db import models

# Create your models here.
class WeekTable(models.Model):
    num=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=12)
    name=models.CharField(max_length=30)
    color=models.CharField(max_length=10)
    etc=models.CharField(max_length=255)
    credit=models.IntegerField()
    professor=models.CharField(max_length=20)
    time=models.JSONField()

    class Meta:
        db_table="weektable"