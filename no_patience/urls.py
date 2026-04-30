from django.urls import path


from . import views

app_name = 'no_patience'
urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
    path('reload/<int:chat_id>/<int:new_chat_query>/', views.reload, name='reload'),
]
