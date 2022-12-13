from django.urls import re_path as path

from . import views

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path(r'^register/$', views.register, name='register'),
    path(r'^myProfile/$', views.my_profile, name='my_profile'),
    path(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    path(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    path(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
    path(r'^user_delete/$', views.UserDelete, name='user_delete'),
    path(r'^user_edit/$', views.update_user, name='user_update')
]


