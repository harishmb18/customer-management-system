from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    company = models.CharField(max_length=200)

    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive")
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ActivityLog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(max_length=50)

    timestamp = models.DateTimeField(auto_now_add=True)