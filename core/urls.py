from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from .views import home
urlpatterns = [

    path("",home,name='home'),
    path("users/",include("book.urls")),
    path('book/<slug:cat_slug>/',home, name = "cat_wise_book"),
    path('book/',home, name = "all_book")
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)