from django.db import models

# Create your models here.

class Vote(models.Model):
	user = models.ForeignKey('user_app.AnyaskUser',on_delete=models.CASCADE,
							related_name='vote'
							)
	answer = models.ForeignKey('ask_app.Answer',on_delete=models.CASCADE)
	agree = models.BooleanField()
	date = models.DateTimeField(auto_now_add=True)

	def voteup(self):
		return Vote.objects.filter(answer=self.answer,agree=True)

	def __str__(self):
		return "<Vote:%s>" % self.answer.title

