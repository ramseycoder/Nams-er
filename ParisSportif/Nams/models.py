from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    contacts = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True, null=True)
    register_date = models.DateTimeField(auto_now_add=True)


class Paries(models.Model):
    equipeA = models.CharField(max_length=100, null=True,unique=True)
    score = models.CharField(max_length=100, verbose_name="scoreA",null=True)
    scoreB = models.CharField(max_length=100, null=True)
    equipeB = models.CharField(max_length=100, null=True,unique=True)
    montant_parié = models.CharField(max_length=100,null=True)
    date_match = models.DateField(null=True)
    v_date_match = models.CharField(max_length=100, null=True)
    date_parie = models.DateTimeField(auto_now_add=True,null=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_parie", null=True)