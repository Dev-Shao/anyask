
from django.db import models
#from user_app import AnyaskUser

# Create your models here.

class Topic(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField(null=True,blank=True)

	def __str__(self):
		return self.title


class Question(models.Model):
	title = models.CharField(max_length=60)
	content = models.TextField(null=True,blank=True)
	asker = models.ForeignKey('user_app.AnyaskUser',related_name='question',
								on_delete=models.SET_NULL,
								null=True,
								blank=True
							)
	topic = models.ManyToManyField('Topic',related_name='question',blank=True)
	visi_count = models.IntegerField(default=0)
#	visitor = models.ManyToManyField('user_app.AnyaskUser',related_name='visit_question',
#									blank=True
#									)
	is_anonymity = models.BooleanField(default=False)
	datetime = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class Answer(models.Model):
	question =  models.ForeignKey('Question',related_name='answer',on_delete=models.CASCADE)
	author = models.ForeignKey('user_app.AnyaskUser',related_name='answer',
								on_delete=models.CASCADE
								)
	content = models.TextField()
	datetime = models.DateTimeField(auto_now_add=True)
	voteup = models.IntegerField(default=0)

	def preview(self):
		return self.content[:120]

	def __str__(self):
		return self.content[:50]


class Comment(models.Model):
	author = models.ForeignKey('user_app.AnyaskUser',related_name='comment',
								on_delete=models.CASCADE
								)
	content = models.TextField()
	reply = models.ForeignKey('user_app.AnyaskUser',related_name='reply_comment',
								on_delete=models.SET_NULL,
								null=True,
								blank=True
								)
	answer = models.ForeignKey('Answer',related_name='comment',on_delete=models.CASCADE,)
	datetime = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.content[:20]



















