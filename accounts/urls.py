"Defines URL patterns for accounts."

from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    # Include default auth urls
    #path('', include('django.contrib.auth.urls')),
    # My url patterns
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('forgot', views.forgot, name='forgot'),
]
