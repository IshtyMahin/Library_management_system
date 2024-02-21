from django import forms
from .models import Book,Category,Review,Deposit

class BookForm(forms.ModelForm):
    class Meta:
        model = Book 
        fields = '__all__'
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["body"]
        
class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields=["amount"]