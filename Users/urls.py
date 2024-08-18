
from django.urls import path, include
from .views import change_data, signup, user_login, user_logout, pass_change, profile

urlpatterns = [
    path('pass_change/', pass_change, name='pass_change'), 
    path('change_data/', change_data, name='change_data'), 
    path('signup/', signup, name='signup'),
    path('user_login/', user_login,name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    path('profile', profile, name='profile')
]
