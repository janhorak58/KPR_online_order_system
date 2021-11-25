from django.db import models
from django.contrib.auth.models import User
import datetime

    
    

class Shipping(models.Model):
    shipping_types = (
        ("Zasilkovna_na_adresu", 'Zásilkovna na adresu'),
        ("Zasilkovna_na_vydejni_misto", 'Zásilkovna na výdejní místo'),
        ("okoli_MH", 'Doručení v okolí Mnichova Hradiště'),
    )
    shipping_type = models.CharField(max_length=90, choices=shipping_types, default="Zasilkovna_na_adresu")
    
    # Fakturační adresa se rovná dodací adrese
    FisD = models.BooleanField(default=True, blank=True)
    


class Address(models.Model):
    address_types = (
        ("fakturacni", 'Fakturační adresa'),
        ("dodaci", 'Dodací adresa'),
    )
    address_type = models.CharField(max_length=90, choices=address_types, default="fakturacni")
    jmeno = models.CharField(max_length=200)
    mesto = models.CharField(max_length=200)
    ulice = models.CharField(max_length=200)
    psc = models.CharField(max_length=10)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, blank=True, null=True)
    

class Order(models.Model):
    number = models.IntegerField(blank=True, null=True, default=0)
    total = models.FloatField(blank=True, null=True, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    month = models.IntegerField(default = datetime.datetime.now().month)
    year = models.IntegerField(default = datetime.datetime.now().year)
    completed_date = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    payment_methods =  (
        ("Comgate_karta", 'Comgate - Karta'),
        ("Comgate_prevod", 'Comgate - Převod'),
        ("Hotove", 'Hotově'),
    )
    payment_method = models.CharField(max_length=90, choices=payment_methods, default="Comgate_karta")
    
    sale = models.IntegerField(null=True, blank=True)
    
    
    note = models.TextField(max_length=1000, blank=True)
    
    states = (
        ("zpracovava_se", 'Objednávka se zpracovává'),
        ("odeslana", 'Objednávka byla odeslána'),
        ("dokoncena", 'Objednávka byla dokončena'),
        ("zrusena", 'Objednávka byla zrušena'),
    )
    state = models.CharField(max_length=90, choices=states, default="zpracovava_se")
    
    through_options = (
        ("pemic", 'Pemic'),
        ("zonerpress", 'E-shop = Zoner-press'),

    )
    through_option = models.CharField(max_length=90, choices=through_options, default="pemic")
    faktura = models.FileField(null=True, blank=True, upload_to='faktury/')
    dodaci_list = models.FileField(null=True, blank=True, upload_to='dodaci_listy/')
    
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, blank=True, null=True)
    
    
    
    def __str__(self):
        return "Objednávka č. " + str(self.id)

class Book(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True, default="")
    author = models.CharField(max_length=300, blank=True, null=True, default="")
    price = models.FloatField(blank=True, null=True, default=0)
    qty = models.IntegerField(blank=True, null=True, default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return str(self.name) + " - " + str(self.author)
    

  

