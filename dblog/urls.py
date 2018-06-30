from django.conf import urls
from dblog.DblogViews import BlogView as views
urlpatterns = [ urls.url(r'^page/(?P<subject_id>[0-9]+)/(?P<pageNum>[0-9]+)$',views.readTopicByPagination, name='readTopicByPagination'),
                 urls.url(r'^topic/(?P<subject_id>[0-9]+)/(?P<topic_id>[0-9]+)$',views.readTopicById, name='readTopicById'),
                urls.url(r'^newTopic$', views.createTopicView.as_view(), name='createTopicView'),
                urls.url(r'^category/(?P<subject_id>[0-9]+)$',views.subjectView.as_view(), name='subjectView'),
                urls.url(r'^editTopic/(?P<subject_id>[0-9]+)/(?P<topic_id>[0-9]+)$',views.editTopicView.as_view(), name='editTopic'),
                urls.url(r'^editDetails/(?P<subject_id>[0-9]+)/(?P<topic_id>[0-9]+)$',views.editDetailsView.as_view(), name='editDetails'),
                
                  ]
