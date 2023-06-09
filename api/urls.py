from django.urls import path #, include
# from django.conf.urls import url

from . import views

urlpatterns = [
    path('aplicant_credit', views.ApplicantCreditView.as_view()),
    path('request_credit', views.RequesCreditView.as_view()),
]