from django.urls import path

from subscribe import views

app_name = 'subscribe'
urlpatterns = [
    path('user', views.SubscribeAuthor.as_view(), name='subscribe_author'),
    path('blog', views.SubscribeBlog.as_view(), name='subscribe_blog'),
]
