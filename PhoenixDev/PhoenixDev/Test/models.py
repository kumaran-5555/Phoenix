from django.db import models

# Create your models here.
class TestTable(models.Model):
    productName = models.CharField(max_length=20)

