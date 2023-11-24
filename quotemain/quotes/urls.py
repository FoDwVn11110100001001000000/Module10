from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path('add_quote/', views.quote, name='add_quote'),
    path('add_author/', views.author, name='add_author'),
    path('author/<str:author_fullname>/', views.author_details, name='author_details'),
]