import uuid
from django.db import models
from pathlib import Path

# Create your models here.


def _obfuscate_uploaded_filename(_instance, filename: str) -> str:
    ext = Path(filename).suffix
    return str(uuid.uuid4()) + ext


class UploadVcf(models.Model):
    file = models.FileField(
        verbose_name="Uploaded Vcf", upload_to=_obfuscate_uploaded_filename
    )
