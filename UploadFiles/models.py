from django.db import models

class MyFileUpload(models.Model):
    
    uploader_name=models.CharField(max_length=50)
    my_file=models.FileField()
    date = models.DateTimeField(null=True,blank=True)
    flour = models.CharField(max_length=1000,default="")
    
