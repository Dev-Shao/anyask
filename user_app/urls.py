
from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<user_id>\d+)/$',views.user_view,name='user'),
	url(r'^login/$',views.login_view,name='login'),
	url(r'^login_/$',views.login_,name='login_'),
	url(r'^logout/$',views.logout_view,name='logout'),
	url(r'^register/$',views.register_view,name='register'),
	url(r'^(?P<user_id>\d+)/activities/$',views.activities,name='activities'),
	url(r'^(?P<user_id>\d+)/answers/$',views.answers,name='answers'),
	url(r'^(?P<user_id>\d+)/questions/$',views.questions,name='questions'),
]
