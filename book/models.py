from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from users.models import UserAccount
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.TextField()
    image = models.ImageField(upload_to="book/media/uploads/", blank=True, null=True)
    description = models.TextField()
    borrowing_price = models.DecimalField(decimal_places=2, max_digits=12)
    quantity = models.IntegerField()
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title

class BorrowHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['borrow_date']

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username}"
    
    def review_book(self, book, body):
        Review.objects.create(user=self.user, book=book, body=body)

class Deposit(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)

