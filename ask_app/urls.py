
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^ask/$',views.ask,name='ask'),
	url(r'^question/(?P<question_id>\d+)/$',views.question_item,name='question'),
	url(r'^question/(?P<question_id>\d+)/answers/$',views.answers,name='answers'),
	url(r'^question/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/$',
		views.answer_item,name='answer'
		),
	url(r'^question/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/comments/$',
			views.comments,name='comments'
		),
	url(r'^question/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/comment/(?P<comment_id>\d+)/$',
			views.comment_item,name='comment'
		),
	url(r'^follow/$',views.follow,name='follow'),
	url(r'^favour/(?P<answer_id>\d+)/$',views.favour,name='favour'),
	url(r'^vote/(?P<answer_id>\d+)/',views.vote,name='vote'),
	url(r'^search/$',views.search,name='search'),
	url(r'^topic/(?P<topic_id>\d+)/$',views.topic,name='topic'),
	url(r'^questions/$',views.questions,name='questions'),
]
