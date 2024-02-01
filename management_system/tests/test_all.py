from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from ..models import BorrowedBooks


class APITestCase(TestCase):
    def setUp(self):
        # Create an API client for making requests
        self.client = APIClient()

    def create_user(self):
        user_data = {
            "Name": "Test User",
            "Email": "test@example.com",
            "MembershipDate": "2024-01-30",
            "password": "Test12345",
        }
        response = self.client.post("/api/users/", user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_data = {
            "email": user_data["Email"],
            "password": user_data["password"],
        }
        login_response = self.client.post("/api/login/", login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data.get("token")

        return response.data["UserID"], token

    def create_book(self, token):
        headers = {"Authorization": f"Token {token}"}

        book_data = {
            "Title": "Test Book",
            "ISBN": "1234567890123",
            "PublishedDate": "2023-01-01",
            "Genre": "Fiction",
            "details": {
                "NumberOfPages": 200,
                "Publisher": "Test Publisher",
                "Language": "English",
            },
        }
        response = self.client.post(
            "/api/books/", book_data, format="json", headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data["BookID"]

    def test_borrowed_books_creation(self):
        # Create a user and a book
        user_id, token = self.create_user()
        book_id = self.create_book(token)

        # Data for creating borrowed books
        borrowed_data = {
            "UserID": user_id,
            "BookID": book_id,
            "BorrowDate": "2024-01-30",
            "ReturnDate": None,
        }

        headers = {"Authorization": f"Token {token}"}

        response = self.client.post(
            "/api/borrowed/", borrowed_data, format="json", headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BorrowedBooks.objects.count(), 1)
        self.assertEqual(BorrowedBooks.objects.get().UserID.UserID, user_id)
        self.assertEqual(BorrowedBooks.objects.get().BookID.BookID, book_id)

    # Add more test methods for other endpoints as needed
