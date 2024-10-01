from django.urls import path
from epub_app import views

app_name = 'epub_app'

urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
    path('epub/<int:pk>/', views.epub_view, name='epub_view'),
    path('epub-list/', views.epub_list, name='epub_list'),  # List of EPUBs with search and pagination
]

