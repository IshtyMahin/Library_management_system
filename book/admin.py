from django.contrib import admin
from .models import Book,Category,BorrowHistory,Review,Deposit
# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(BorrowHistory)
admin.site.register(Review)
admin.site.register(Deposit)