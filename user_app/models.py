from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class AnyaskUser(AbstractUser):
	brief = models.CharField(max_length=50,null=True,blank=True)
	image = models.ImageField(upload_to='image/user/',default='image/user/default.png')
	location = models.CharField(max_length=100,null=True,blank=True)
	industry = models.CharField(max_length=100,null=True,blank=True)
	follow_question = models.ManyToManyField('ask_app.Question',blank=True)
	follow_topic = models.ManyToManyField('ask_app.Topic',blank=True)
	follow_user = models.ManyToManyField('self',blank=True)
	favour_answer = models.ManyToManyField('ask_app.Answer',blank=True)

	
