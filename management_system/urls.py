# urls.py

from django.urls import path
from .views import (
    UserListCreateView,
    UserDetailsView,
    BookListCreateView,
    BookDetailsView,
    BorrowedBooksListCreateView,
    BorrowedBooksDetailsView,
)
from .views import TokenObtainPairView

urlpatterns = [
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:UserID>/", UserDetailsView.as_view(), name="user-details"),
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("books/<int:BookID>/", BookDetailsView.as_view(), name="book-details"),
    path(
        "borrowed/",
        BorrowedBooksListCreateView.as_view(),
        name="borrowed-books-list-create",
    ),
    path(
        "borrowed/<int:pk>/",
        BorrowedBooksDetailsView.as_view(),
        name="borrowed-books-details",
    ),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]
