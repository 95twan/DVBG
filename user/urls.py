from django.urls import path
from user.views import SelfRegister, OAuthRegister, SelfLogin, OAuthLogin

app_name = 'user'
urlpatterns = [
    path('selfregister/', SelfRegister.as_view(), name='self_register'),
    path('oauthregister/', OAuthRegister.as_view(), name='oauth_register'),
    path('selflogin/', SelfLogin.as_view(), name='self_login'),
    path('oauthlogin/', OAuthLogin.as_view(), name='oauth_login'),
]
