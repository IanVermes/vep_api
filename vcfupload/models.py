import uuid
from django.db import models
from pathlib import Path

# Create your models here.


def _obfuscate_uploaded_filename(instance, filename: str) -> str:
    "Record the original filename and obfuscate the filename as stored in the DB"
    instance.original_filename = filename
    ext = Path(filename).suffix
    return str(uuid.uuid4()) + ext


class UploadVcf(models.Model):
    file = models.FileField(
        verbose_name="Uploaded Vcf", upload_to=_obfuscate_uploaded_filename,
    )

    original_filename = models.CharField(
        verbose_name="Filename as POSTed by user", max_length=255, blank=True
    )
