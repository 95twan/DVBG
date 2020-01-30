from django.urls import path
from blog.views import BoardList, BoardDetail, PostList, PostDetail

urlpatterns = [
    path('board/', BoardList.as_view(), name='board_list'),
    path('board/<int:pk>/', BoardDetail.as_view(), name='board_detail'),
    path('post/', PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
]
