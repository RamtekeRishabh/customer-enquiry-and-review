from django.contrib import admin
from django.urls import path, include
from main_app import views

urlpatterns = [
    path('', views.enquiry, name='customer-enquiry'),
    path('query_submit', views.query_submit, name='submit-customer-enquiry'),
    path("enquiry_detail/<id>", views.enquiry_detail, name ="enquiry-detail"),
    path("response_submit/<id>", views.response_submit, name ="response-submit"),
    path('review/<id>', views.review, name='review'),
    path('review_submit/<id>', views.review_submit, name='submit-customer-review'),
    # path("response_submit/<id>", views.response_submit, name ="response-submit"),
]