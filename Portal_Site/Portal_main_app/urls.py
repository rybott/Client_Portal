from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.main, name="main"),
    path('case/<int:pk>/', views.case_detail, name='case_detail'),
    path('intake', views.case_intake, name="case_intake"),
    path('lawyer/create/', views.lawyer_create_form, name='lawyer_create_form'),
    path('lawyer/autocomplete/', views.lawyer_autocomplete, name='lawyer_autocomplete'),
    path('case/<int:case_id>/note/', views.case_note_create, name='case_note_create'),
    path("case/<int:pk>/tasks/", views.case_tasks_list, name="case_tasks_list"),
    path('case/<int:pk>/task/new/', views.task_create_form, name='task_create_form'),
    path('case/<int:pk>/task/modal/new/', views.task_modal_create, name='task_modal_create'),

]