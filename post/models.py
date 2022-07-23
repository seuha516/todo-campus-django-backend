from django.db import models

# Create your models here.
class Post(models.Model):
    num=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=12)
    nickname=models.CharField(max_length=8)
    title=models.CharField(max_length=30)
    body=models.TextField()
    image=models.JSONField()
    tag=models.JSONField()
    comment=models.JSONField()
    like=models.JSONField()
    publishedDate=models.DateTimeField()
    lastModifiedDate=models.DateTimeField()

    class Meta:
        db_table="post"