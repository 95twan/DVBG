from django.urls import path
from user.views import SelfRegister, OAuthRegister

app_name = 'user'
urlpatterns = [
    path('selfregister/', SelfRegister.as_view(), name='self_register'),
    path('oauthregister/', OAuthRegister.as_view(), name='oauth_register'),
]
