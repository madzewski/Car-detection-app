from django.urls import path
from .views import CarDetectionView, index

urlpatterns = [
    path('', index, name='index'),
    path('detect/', CarDetectionView.as_view(), name='car-detection'),
]