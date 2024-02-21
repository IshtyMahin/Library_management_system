from django.shortcuts import render
from book.models import Category,Book
# Create your views here.
def home(request,cat_slug=None):
    data = Book.objects.all()
    
    if cat_slug is not None:
        data = Book.objects.filter(categories__slug=cat_slug)
        
    categories = Category.objects.all()
    return render(request, 'index.html', {'data': data, 'categories':categories})