from django.db import models

# Create your models here.
class Todo(models.Model):
    num=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=12)
    title=models.CharField(max_length=30)
    category=models.CharField(max_length=8)
    noted=models.IntegerField()
    due=models.DateTimeField()

    class Meta:
        db_table="todo"