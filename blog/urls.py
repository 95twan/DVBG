from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('board/', views.BoardList.as_view(), name='board_list'),
    path('board/<int:pk>/', views.BoardDetail.as_view(), name='board_detail'),
    path('post/', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('comment/', views.CommentList.as_view(), name='comment_list'),
    path('comment/<int:pk>/', views.CommentDetail.as_view(), name='comment_detail'),
]
