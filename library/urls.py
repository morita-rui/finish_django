from django.urls import path
from .views import DetailView, IndexView

app_name = 'library'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', DetailView.as_view(), name='detail'),
]
