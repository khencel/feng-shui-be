from django.db import models

# Create your models here.
class Combination(models. Model):
    id = models.AutoField(primary_key=True)
    first_num = models.CharField(max_length=10, null=True, blank=True)
    second_num = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "combination"
    