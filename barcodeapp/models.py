from django.db import models

class Barcode(models.Model):
    code = models.CharField(max_length=100)
    image = models.ImageField(upload_to='barcodes/')
