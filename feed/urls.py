from django.urls import path
from feed import views

app_name = 'feed'
urlpatterns = [
    path('feeds', views.FeedView.as_view(), name='feed'),
    path('feeds/<int:user_id>', views.FeedDetailView.as_view(), name='feed_detail'),
]
