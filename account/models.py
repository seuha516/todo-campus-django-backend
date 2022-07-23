from django.db import models

# Create your models here.
class Account(models.Model):
    username=models.CharField(max_length=12, primary_key=True)
    hashedPassword=models.CharField(max_length=255)
    email=models.CharField(max_length=45)
    nickname=models.CharField(max_length=8)
    setting=models.JSONField()
    notice=models.JSONField()

    class Meta:
        db_table="account"