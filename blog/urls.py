from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('boards', views.BoardList.as_view(), name='board_list'),
    path('boards/<int:pk>', views.BoardDetail.as_view(), name='board_detail'),
    path('posts', views.PostList.as_view(), name='post_list'),
    path('posts/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('comments', views.CommentList.as_view(), name='comment_list'),
    path('comments/<int:pk>', views.CommentDetail.as_view(), name='comment_detail'),
]
