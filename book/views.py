from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Book, BorrowHistory, Deposit, Review
from .forms import ReviewForm, DepositForm
from django.contrib import messages
from users.models import UserAccount
from django.utils import timezone


class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'book_list.html', {'books': books})

class BookDetailView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        has_borrowed = BorrowHistory.objects.filter(user=request.user, book=book,return_date__isnull=True).exists()
        count = BorrowHistory.objects.filter(user=request.user, book=book).count()
        reviews = Review.objects.filter(book=book)
        reviews_form = ReviewForm()
        return render(request, 'book_details.html', {'book': book, 'has_borrowed': has_borrowed, 'reviews': reviews, 'reviews_form': reviews_form,'count': count})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(user=request.user, book=book, body=form.cleaned_data['body'])
            messages.success(request, "Review added successfully.")
        else:
            messages.error(request, "Invalid form submission.")
        return redirect('detail_book', pk=pk)

class BorrowBookView(View):
    def get(self, request, pk):
            user = request.user
            book = get_object_or_404(Book, pk=pk)
         
            borrowing_price = book.borrowing_price
            user_account = UserAccount.objects.get(user=user)
            if user_account.balance >= borrowing_price:
                borrow = BorrowHistory.objects.create(user=user, book=book)
                
                user_account.balance -= borrowing_price
                user_account.save()
                messages.success(request,"Book successfully borrowed")
            else:
                messages.error(request,"Insufficient balance")
                
            return redirect('detail_book', pk=pk)

class ReturnBookView(View):
    def get(self, request, pk):
        user = request.user
        book = get_object_or_404(Book, pk=pk)
        borrow = BorrowHistory.objects.get(user=user, book=book,return_date__isnull=True)
        if borrow:
            borrow.return_date = timezone.now() 
            borrow.save() 
            user_account = UserAccount.objects.get(user=user)
            user_account.balance += book.borrowing_price
            user_account.save()
            
            messages.success(request, "Book successfully returned")
        else:
            messages.error(request, "No active borrowing record found for this book")
        
        return redirect('detail_book', pk=pk)

class BorrowedBooksView(View):
    def get(self, request):
        user = request.user
        borrowed_books = BorrowHistory.objects.filter(user=user,return_date__isnull=True)
        print(borrowed_books)
        returned_books = BorrowHistory.objects.filter(user=user,return_date__isnull=False)
        
        return render(request, 'borrow_history.html', {'borrowed_books': borrowed_books, 'returned_books': returned_books})


class DepositMoneyView(View):
    def get(self, request):
        form = DepositForm()
        return render(request, 'deposit_money.html', {'form': form})

    def post(self, request):
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = request.user.account
            account.balance += amount
            account.save()
            messages.success(request, "Deposit was successful.")
            return redirect('deposit_money')
        else:
            messages.error(request, "Invalid form submission.")
            return render(request, 'deposit_money.html', {'form': form})


def borrowing_history(request):
    borrows = BorrowHistory.objects.filter(user=request.user)
    return render(request, 'borrowing_history.html', {'borrows': borrows})



        