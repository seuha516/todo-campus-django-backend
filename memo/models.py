from django.db import models

# Create your models here.
class Memo(models.Model):
    num=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=12)
    body=models.TextField()

    class Meta:
        db_table="memo"