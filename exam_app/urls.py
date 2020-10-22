from django.urls import path 
from . import views



urlpatterns = [
    path('', views.index),
    path('addUser', views.addUser),
    path('thoughts', views.thoughts),
    path('login', views.login),
    path('logout', views.logout),
    path('addThought', views.addThought),
    path('thoughts/<int:thought_id>', views.thoughtInfo),
    path('destroy/<int:thought_id>', views.destroyThought),
    path('like/<int:user_id>/<int:thought_id>', views.likes),
    path('unlike/<int:user_id>/<int:thought_id>', views.unlikes)
]