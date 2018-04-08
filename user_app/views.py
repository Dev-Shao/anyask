from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .models import AnyaskUser
from profile_app.models import Vote
from ask_app.models import Question,Topic
import json

# Create your views here.
#get_object_or_404()

def login_view(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username,password=password)
		if user and user.is_active:
			login(request,user)
			return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	context = {}
	return render(request,'user_app/login.html',context)


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('ask_app:index'))


def login_(request):
	if request.method == "POST":
		result = {'result':'error'}
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username,password=password)
		if user and user.is_active:
			login(request,user)	
			result['result'] = 'success'
			return HttpResponse(json.dumps(result))
		return HttpResponse(json.dumps(result))
	context = {}
	return render(request,'user_app/login.html',context)


def register_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		if not AnyaskUser.objects.filter(username=username):
			if password1 == password2:
				new_user = AnyaskUser.objects.create_user(username,email,password1)
				new_user.save()
				login(request,new_user)
				return HttpResponseRedirect(reverse('ask_app:index'))
	return HttpResponseRedirect(reverse('user_app:login'))

#@login_required
def user_view(request,user_id):
	user = AnyaskUser.objects.get(pk=user_id)
	answers = user.answer.all()
	votes = user.vote.all().order_by('-date')
	context = {'user':user,'answers':answers,'votes':votes}
	return render(request,'user_app/user.html',context)


def answers(request,user_id):
	user = AnyaskUser.objects.get(pk=user_id)
	answers = user.answer.all().order_by('-datetime')
	context = {'answers':answers}
	return render(request,'user_app/answer_item.html',context)


def questions(request,user_id):
	user = AnyaskUser.objects.get(pk=user_id)
	questions = user.question.all().order_by('-datetime')
	context = {'questions':questions}
	return render(request,'user_app/question_item.html',context)


def activities(request,user_id):
	user = AnyaskUser.objects.get(pk=user_id)
	votes = user.vote.all().order_by('-date')
	context = {'votes':votes}
	return render(request,'user_app/activities_item.html',context)


