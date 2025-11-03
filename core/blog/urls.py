# blog/urls.py

from django.urls import path
from .views import blog_list_view, blog_detail_view

urlpatterns = [
    path('', blog_list_view, name='blog'),
    path('<slug:slug>/', blog_detail_view, name='blog-detail'),

]