from django.db import models

# Create your models here.

class Entries(models.Model):
    positive = models.IntegerField(default=0)
    negative = models.IntegerField(default=0) 
    neutral = models.IntegerField(default=0)
    confidence = models.FloatField(default=None,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    audio_name = models.CharField(null=True,max_length=50)
    audio_file = models.FileField(upload_to='audio',blank=True,null=True)

    def __str__(self) -> str:
        return super().__str__()
