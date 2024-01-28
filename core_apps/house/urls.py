from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateHouseView.as_view()),
    path('list/', views.ListHouseView.as_view()),
    path('<uuid:id>/update', views.UpdateHouseView.as_view()),
    path('<uuid:id>/delete', views.DeleteHouseView.as_view()),
    path('<uuid:id>/users/<str:phone_number>/add', views.AddUserToHouseView.as_view()),
]
