from django.conf.urls import patterns, url, include

from support import views
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^school/(?P<grade_group_id>\d+)/$', views.grade_group, name='grade_group'),
    url(r'^lesson/(?P<lesson_id>\d+)/$', views.lesson, name='lesson'),
    url(r'^create_post/(?P<lesson_category_id>\d+)/$', views.create_post, name='create_post'),
    url(r'^post/(?P<post_id>\d+)/up_vote/$', views.up_vote, name='up_vote'),
    url(r'^post/(?P<post_id>\d+)/down_vote/$', views.down_vote, name='down_vote'),
    url(r'^post/(?P<post_id>\d+)/edit/$', views.edit_post, name='edit_post'),
    url(r'^post/(?P<post_id>\d+)/flag/$', views.flag_post, name='flag_post'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^forum/(?P<forum_id>\d+)/upload_supplemental_material/$', 
        views.upload_supplemental_material, name='upload_supplemental_material'),
    url(r'^user/(?P<user_id>\d+)/$', views.user, name='user'),
    url(r'^search/', include('haystack.urls')),
)
