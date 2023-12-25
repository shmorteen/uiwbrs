from django.db import models

# Create your models here.
class UserRecord(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	user_type = models.CharField(max_length=3)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)
	location = models.CharField(max_length=50)
	
	def __str__(self):
		return(f"{self.first_name} {self.last_name}")
	
class Item(models.Model):
    namee = models.CharField(max_length=100)
	
class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
