from django.conf.urls import patterns, url

from support import views
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^grade/(?P<grade_id>\d+)/$', views.grade, name='grade'),
    url(r'^topic/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    url(r'^topic/grade/(?P<topic_grade_id>\d+)/$', views.topic_grade, name='topic_grade'),
    url(r'^lesson/(?P<lesson_id>\d+)/$', views.lesson, name='lesson'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^answer/$', views.answer, name='answer'),
    url(r'^question/(?P<question_id>\d+)/up_vote/$', views.up_vote_question, 
        name='up_vote_question'),
    url(r'^question/(?P<question_id>\d+)/down_vote/$', views.down_vote_question, 
        name='down_vote_question'),
    url(r'^answer/(?P<answer_id>\d+)/up_vote/$', views.up_vote_answer, 
        name='up_vote_answer'),
    url(r'^answer/(?P<answer_id>\d+)/down_vote/$', views.down_vote_answer, 
        name='down_vote_answer'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^lesson/(?P<lesson_id>\d+)/upload_supplemental_material/$', 
        views.upload_supplemental_material, name='upload_supplemental_material'),
    url(r'^user/(?P<user_id>\d+)/$', views.user, name='user'),
)
