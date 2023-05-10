from decimal import Decimal
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Investor(models.Model):
    RISK_PROFILE_CHOICES = (
        ('C', 'Conservador'),
        ('M', 'Moderado'),
        ('A', 'Arrojado'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    risk_profile = models.CharField(max_length=1, choices=RISK_PROFILE_CHOICES)

    def __str__(self):
        return self.user.username

class Stock(models.Model):
    code = models.CharField(max_length=6)
    name_enterprise = models.CharField(max_length=90)
    cnpj = models.CharField(max_length=18)

    def __str__(self):
        return "{} - {}".format(self.code, self.name_enterprise)

class Transaction(models.Model):
    TYPE_OF_TRANSACTION = (
        ('C', 'Compra'),
        ('V', 'Venda'),
    )
    date_done = models.DateField(default=datetime.now, blank=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity_stock = models.PositiveIntegerField()
    unite_price = models.FloatField()
    type_of = models.CharField(max_length=1, choices=TYPE_OF_TRANSACTION)
    brokerage = models.FloatField()
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)

# traduzir os metodos
    def valor_compra(self):
        valor = self.quantity_stock * self.unite_price 
        return round(valor, 2)
    
    def valor_total_transaction(self):
        if self.TYPE_OF_TRANSACTION == 'C':
            valor_total = self.valor_compra() + self.brokerage
        else:
            valor_total = self.valor_compra() - self.brokerage
        
        return round(valor_total, 2)

    def __str__(self):
        return '{}-{}'.format(self.stock,self.type_of)