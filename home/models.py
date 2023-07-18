from django.db import models


# Create your models here.


class CowinData(models.Model):
    center_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    fee_type = models.CharField(max_length=100)
    fee = models.IntegerField(default=0)
    available_capacity = models.CharField(max_length=100)
    available_capacity_dose1 = models.IntegerField(default=0)
    available_capacity_dose2 = models.IntegerField(default=0)
    min_age_limit = models.IntegerField(default=45)
    vaccine = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.pincode


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"id: {self.id}  Number: {self.phone_number}"
