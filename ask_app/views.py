from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from user_app.models import AnyaskUser
from profile_app.models import Vote
from .models import Topic,Question,Answer,Comment
from .forms import QuestionForm,AnswerForm
import json

# Create your views here.
def is_login(func):
	def g(*args,**kw):
		if not args[0].user.is_authenticated():
			print('it not login')
			return HttpResponse(json.dumps({'result':'unlogin','data':''}))
		return func(*args,**kw)
	return g


def index(request):
	answer_list = Answer.objects.all().order_by('-datetime')
	paginator = Paginator(answer_list,5)
	page = request.GET.get('page',False)
	if not page:
		answers = paginator.page(1)
		context = {'answers':answers}
		return render(request,'ask_app/index.html',context)
	try:
		answers = paginator.page(page)
	except PageNotAnInteger:
		answers = paginator.page(1)
	except EmptyPage:
		return HttpResponse()

	context = {'answers':answers}
	return render(request,'ask_app/answeritem.html',context)

'''
def question(request,question_id):
	question = Question.objects.get(pk=question_id)

	answer_list = question.answer_set.all().order_by('-voteup')
	paginator = Paginator(answer_list,5)
	page = request.GET.get('page',False)
	if not page:
		answers = paginator.page(1)
		context = {'question':question,'answers':answers}
		return render(request,'ask_app/question.html',context)
	try:
		answers = paginator.page(page)
	except PageNotAnInteger:
		answers = paginator.page(1)
	except EmptyPage:
		return HttpResponse()
		
	context = {'answers':answers}
	return render(request,'ask_app/item.html',context)
'''

def questions(request):
	questions = Question.objects.all().order_by('-datetime')
	context = {'questions':questions}
	return render(request,'ask_app/questions.html',context)
	


def question_item(request,question_id):
	# url /question/(question_id)/

	question = Question.objects.get(pk=question_id)
	
	if not request.session.get(question_id,False):
		request.session[question_id] = True
		question.visi_count += 1
		question.save()

	if request.method == "GET":
		pass
	elif request.method == "POST":
		method = request.POST.get('_method')
		if method == 'delete':
			Question.objects.remove(question)
			return HttpResponse()
		else:
			pass
	answers = question.answer.all().order_by('-voteup')[:5]
	context = {'question':question,'answers':answers}
	return render(request,'ask_app/question.html',context)	



def answers(request,question_id):
	# url /question/(question_id)/answers/

	question = Question.objects.get(pk=question_id)
	if request.method == 'GET':
		answer_list = question.answer.all().order_by('-voteup')
		paginator = Paginator(answer_list,5)
		page = request.GET.get('page',1)
		answers = []
		try:
			answers = paginator.page(page)
		except PageNotAnInteger:
			answers = paginator.page(1)
		except EmptyPage:
			return HttpResponse()
		context = {'answers':answers}
		return render(request,'ask_app/item.html',context)

	elif request.method == 'POST':
		content = request.POST.get('content')
		if content.strip():
			new_answer = Answer(question=question,author=request.user,content=content)
			new_answer.save()
			return HttpResponseRedirect(reverse('ask_app:question',args=(question_id)))


def answer_item(request,question_id,answer_id):
	# url /question/(question_id)/answer/(answer_id)/

#	question = Question.objects.get(pk=question_id)
	answer = Answer.objects.get(pk=answer_id)
	question = answer.question
	if request.method == "GET":
		pass
	elif request.method == "POST":
		method = request.POST.get('_method')
		if method == 'delete':
			Answer.objects.remove(answer)
			return HttpResponse()
		else:
			content = request.POST.get('content')
			answer.content = content
			answer.save()
	comments = answer.comment.all().order_by('-datetime')[:5]	
	context = {'question':question,'answer':answer,'comments':comments}
	return render(request,'ask_app/answer.html',context)


@login_required
def ask(request):
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			new_question = form.save(commit=False)
			new_question.asker = request.user
			new_question.save()
			return HttpResponseRedirect(reverse('ask_app:question',args=(str)(new_question.id)))
	context = {}
	return render(request,'ask_app/ask.html',context)


@login_required
def answer(request,question_id):
	question = Question.objects.get(pk=question_id)
	if request.method == 'POST':
		content = request.POST.get('content')
		if content.strip():
			new_answer = Answer(question=question,author=request.user,content=content)
			new_answer.save()
			return HttpResponseRedirect(reverse('ask_app:question',args=question_id))
	context = {'question':question}
	return render(request,'ask_app/answer.html',context)


def comments(request,question_id,answer_id):
	# url /question/(question_id)/answer/(answer_id)/comments/

	answer = Answer.objects.get(pk=answer_id)
	comments = {}
	if request.method == 'POST':
		content = request.POST.get('content')
		if content and content.strip():
			new_comment = Comment(author=request.user,content=content,answer=answer)
			new_comment.save()
		#	comments = [new_comment]
			return HttpResponseRedirect(reverse('ask_app:answer',args=(question_id,answer_id)))
	elif request.method == 'GET':
		page = request.GET.get('page',1)
		comment_list = answer.comment.all().order_by('-datetime')
		paginator = Paginator(comment_list,5)
		try:
			comments = paginator.page(page)
		except PageNotAnInteger:
			comments = paginator.page(1)
		except EmptyPage:
			return HttpResponse()
	context = {'comments':comments}
	return render(request,'ask_app/commentitem.html',context)


def comment_item(request,q_id,a_ia,comment_id):
	# url /question/(q_id)/answer/(a_ia)/comment/(comment_id)/

	comment = Comment.objects.get(pk=comment_id)
	if request.method == "GET":
		op = request.GET.get('op',False)
		if op == 'edit':
			pass
		else:
			pass
	elif request.method == "POST":
		method = request.POST.get('_method')
		if method == 'delete':
			Comment.objects.remove(comment)
			return HttpResponse()
		else:
			content = request.POST.get('content')
			comment.content = content
			comment.save()
	comments = [comment]
	context = {'comments':comments}
	return render(request,'ask_app/commentitem.html',context)


@is_login
def follow(request):
	data = dict(result='ok',reason='ok')
	follow_object = request.GET.get('object',None)
	object_id = request.GET.get('id',None)
	context = {}
	if follow_object and object_id:
		if follow_object.lower() == 'question':
			question = Question.objects.get(pk=object_id)
			follow_question = request.user.follow_question.all()
			if question in follow_question:
				request.user.follow_question.remove(question)
				context = {'result':'unfollow'}
			else:
				request.user.follow_question.add(question)
				context = {'result':'follow'}
			
		elif follow_object.lower() == 'topic':
			topic = Topic.objects.get(pk=object_id)
			follow_topic = request.user.follow_topic.all()
			if topic in follow_topic:
				request.user.follow_topic.remove(topic)
				context = {'result':'unfollow'}
			else:
				request.user.follow_topic.add(follow_object)
				context = {'result':"unfollow"}

		elif follow_object.lower() == 'user':
			anyaskuser = AnyaskUser.objects.get(pk=object_id)
			follow_user = request.user.follow_user.all()
			if usr in follow_user:
				request.user.follow_user.remove(anyaskuser)
				context = {'result':"unfollow"}
			else:
				request.user.follow_user.add(anyaskuser)
				context = {'result':'follow'}
		request.user.save()
	return HttpResponse(json.dumps(context))


@is_login
def favour(request,answer_id):
	answer = Answer.objects.get(pk=answer_id)
	favour_answer = request.user.favour_answer.all()
	if answer in favour_answer:
		request.user.favour_answer.remove(answer)
		context = {'result':'unfavour'}
	else:
		request.user.favour_answer.add(answer)
		request.user.save()
		context = {'result':'favour'}
	return HttpResponse(json.dumps(context))

@is_login
def vote(request,answer_id):
	op = request.GET.get('op')
	answer = Answer.objects.get(pk=answer_id)
	if op == 'up':
		votes = answer.vote_set.filter(user=request.user)
		if votes:
			vote = votes[0]
			if not vote.agree:
				vote.agree = True
				vote.save()
				answer.voteup += 1
				answer.save()
		else:	
			v = Vote(user=request.user,agree=True,answer=answer)
			v.save()
			answer.voteup += 1
			answer.save()
		
	elif op == 'down':
		votes = answer.vote_set.filter(user=request.user)
		if votes:
			vote = votes[0]
			if vote.agree:
				vote.agree = False
				vote.save()
				answer.voteup -= 1
				answer.save()
		else:
			v = Vote(user=request.user,agree=False,answer=answer)
			v.save()
			answer.voteup -= 1
			answer.save()
	else:
		HttpResponse(False)
	result = {'data':answer.voteup}
	return HttpResponse(json.dumps(result))


def search(request):
	if request.method == "GET":
		kw = request.GET.get('search')
		if kw and kw.strip():
			questions = Question.objects.filter(title__icontains=kw)
			context = {'questions':questions,'kw':kw}
			return render(request,'ask_app/search.html',context)
	return HttpResponseRedirect('/')

def topic(request,topic_id):
	topic = Topic.objects.get(pk=topic_id)
	questions = topic.question.all()
	context = {'questions':questions,'topic':topic}
	return render(request,'ask_app/topic.html',context)










