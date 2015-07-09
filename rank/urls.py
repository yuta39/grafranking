from django.conf.urls import patterns, include, url
from rank import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$',views.home, name='home'),
    url(r'^event/$',views.VoteEventList.as_view(),name='eventList'),
    url(r'^event/ranking/(?P<event_id>\d+)/$',views.eventRanking,name='eventRanking'),
    url(r'^event/add/$',views.eventAdd,name='eventAdd'),
    url(r'^event/del/(?P<event_id>\d+)/$',views.eventDel,name='eventDel'),
    url(r'^event/vote/(?P<event_id>\d+)/$',views.eventVote,name='eventVote'),
    url(r'^event/mod/(?P<event_id>\d+)/$',views.eventEdit,name='eventEdit'),
)
