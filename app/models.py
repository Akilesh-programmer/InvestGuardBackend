from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=255,blank=False,null=False)
    email = models.EmailField(null=False,blank=False)
    password = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.username

class Stock(models.Model):
    symbol = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.symbol} - {self.name}"
class InvestModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    company = models.ForeignKey(Stock,on_delete=models.CASCADE)
    stock_unit = models.IntegerField(null=False)
    base_price = models.IntegerField(default=0)

    @property
    def total_price(self):
        return self.stock_unit * self.base_price
    
class NewsHeadLines(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    headline = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline[:100]
    



class UserCompany(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    companies_news = models.TextField()

    def __str__(self):
        return f"{self.user}"
    


class ResponseModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    response_Text = models.TextField()

    def __str__(self):
        return f"{self.user} -- {self.response_Text}"