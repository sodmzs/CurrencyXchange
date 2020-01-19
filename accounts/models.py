from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class balance(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	balance = models.IntegerField(default = 0)

	def __str__(self):
		return self.user.username

class UserProfile(models.Model):
	user =models.OneToOneField(User, on_delete= models.CASCADE)
	website = models.URLField(default='')
	picture = models.ImageField(default='profile_image/profile_avatar.jpg', upload_to='profile_image', blank=True)

	def __str__(self):
		return self.user.username



