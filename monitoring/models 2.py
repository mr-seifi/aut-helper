from django.db import models

# Create your models here.
class Monitor(models.Model):
    name = models.CharField(max_length=100)
    u = models.DecimalField()
    core = models.SlugField()
    
    def __str__(self) -> str:
        return self.name
