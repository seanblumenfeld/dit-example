from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CASCADE
from viewflow.models import Process

from grants.settings import AMOUNT_DECIMAL_PRECISION


class ApplicationProcess(Process):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    proposal = models.TextField()
    requested_amount = models.DecimalField(
        validators=[MinValueValidator(Decimal('0.01'))], **AMOUNT_DECIMAL_PRECISION
    )
    legal_approved = models.BooleanField(default=False)
    finance_approved = models.BooleanField(default=False)


class ApplicationNotes(models.Model):
    application_process = models.ForeignKey(ApplicationProcess, on_delete=CASCADE)
    notes = models.TextField()
