from care.utils.models.base import BaseModel
from django.db import models


class AbhaNumber(BaseModel):
    abha_number = models.TextField(null=True, blank=True, unique=True)
    health_id = models.TextField(null=True, blank=True, unique=True)

    patient = models.OneToOneField(
        "facility.PatientRegistration",
        related_name="abha_number",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    name = models.TextField(null=True, blank=True)
    first_name = models.TextField(null=True, blank=True)
    middle_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)

    gender = models.TextField(null=True, blank=True)
    date_of_birth = models.TextField(null=True, blank=True)

    address = models.TextField(null=True, blank=True)
    district = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    pincode = models.TextField(null=True, blank=True)

    email = models.EmailField(null=True, blank=True)
    profile_photo = models.TextField(null=True, blank=True)

    new = models.BooleanField(default=False)

    txn_id = models.TextField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.pk} {self.abha_number}"