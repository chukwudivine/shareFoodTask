from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('filter/', views.queryfilter, name='filter'),
    path('like/<int:recipe_id>/', views.like, name='like'),

]
