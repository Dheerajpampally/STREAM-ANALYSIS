from django.urls import path
from . import views

urlpatterns = [
    path('chat/home/', views.chat_home, name = 'chat_home'),
    path('chat/box/<int:id>/', views.chat_box, name = 'chat_box'),

    path('notification/counsellor/', views.counsellor_notifications, name = 'counsellor_notifications'),
    path('notification/counsellor/read/<int:id>', views.counsellor_mark_as_read, name = 'counsellor_mark_as_read'),
    
    path('notification/agency/', views.agency_notifications, name = 'agency_notifications'),
    path('notification/agency/read/<int:id>', views.agency_mark_as_read, name = 'agency_mark_as_read'),

    path('select/agent/<int:score>/', views.select_agent, name = 'select_agent'),
    path('select/agent/<int:score>/<int:id>/', views.select_agent_complete, name = 'select_agent_complete'),

    path('select/college/<int:score>/', views.select_college, name = 'select_college'),
    path('select/college/<int:score>/<int:id>/', views.select_college_complete, name = 'select_college_complete'),


]
