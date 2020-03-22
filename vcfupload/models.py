from django.db import models

# Create your models here.


class UploadVcf(models.Model):
    file = models.FileField(verbose_name="Uploaded Vcf")
