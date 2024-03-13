from django.urls import path
from . import views
from .views import UploadFile

urlpatterns = [
    path('upload/', UploadFile.as_view(), name='upload_file'),
    path('budget/', views.get_budget_names, name='get_budget_names'),
    path('categories/', views.get_category_names, name='get_category_names'),
    path('update_category_budget/', views.update_category_budget, name='update_category_budget')
]
