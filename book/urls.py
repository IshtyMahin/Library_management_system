from django.contrib import admin
from django.urls import path,include
from .views import DepositMoneyView,BookDetailView,BorrowBookView,ReturnBookView,BorrowedBooksView
urlpatterns = [

    path("deposit/",DepositMoneyView.as_view(),name='deposit_money'),
    path('details/<int:pk>',BookDetailView.as_view(),name='detail_book'),
    path('borrow/<int:pk>',BorrowBookView.as_view(),name='borrow_book'),
    path('return/<int:pk>',ReturnBookView.as_view(),name='return_book'),
    path('history/',BorrowedBooksView.as_view(),name='history')
]
