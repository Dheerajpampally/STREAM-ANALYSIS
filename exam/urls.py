from django.urls import path
from . import views

urlpatterns = [
    path('stream/select/', views.pick_exam_stream, name='pick_exam_stream'),
    path('ajax/get/stream/<int:id>/', views.get_stream_from_course, name='get_stream_from_course'),
    path('ajax/get/substream/<int:id>/', views.get_substream_from_stream, name='get_substream_from_stream'),

    path('testpage/<int:course>/<stream>/', views.exam_view, name='testpage'),
    path('completed/', views.exam_completed, name='exam_completed'),
    path('history/', views.exam_history, name='exam_history')
]
