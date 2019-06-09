from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('role/', views.role, name='role'),
    path('stuPredict/', views.student, name='student'),
    path('stuPredict/ssa/', views.wrong, name='wrong'),
    path('select_group/', views.select_group, name='select_group'),
    path('select_group/it/', views.select_IT, name='selectIT'),
    path('select_group/dsba/', views.select_DSBA, name='selectDSBA'),
    path('select_group/personal/', views.student, name='personal'),

]
