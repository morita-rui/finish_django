from django.urls import path
from .views import DetailView, IndexView, CreateView, UpdateView, DeleteView, BorrowView, ReturnView, MyLoansView, ReviewView, CreateReviewView

app_name = 'library'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', DetailView.as_view(), name='detail'),
    path('create/', CreateView.as_view(), name='create'),
    path('<int:pk>/update/', UpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', DeleteView.as_view(), name="delete"), 
    path('<int:pk>/borrow/', BorrowView.as_view(), name='borrow'),
    path('<int:pk>/return/', ReturnView.as_view(), name='return'),
    path('<int:pk>/review/', ReviewView.as_view(), name='review'),
    path('<int:pk>/review/create/', CreateReviewView.as_view(), name='review_create'),
    path('my-loans/', MyLoansView.as_view(), name='my_loans'),
]
