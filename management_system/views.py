# views.py
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import User, Book, BookDetails, BorrowedBooks
from .serializers import (
    UserSerializer,
    BookSerializer,
    BookDetailsSerializer,
    BorrowedBooksSerializer,
    UserTokenSerializer,
    TokenResponseSerializer,
)
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Override perform_create to set the password using set_password
        password = self.request.data.get("password")
        serializer.save(password=password)

    def get_queryset(self):
        # Override get_queryset to exclude password field
        return super().get_queryset().exclude(password__isnull=True)


class UserDetailsView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "UserID"


class TokenObtainPairView(APIView):
    @extend_schema(
        request=UserTokenSerializer,
        responses={status.HTTP_200_OK: TokenResponseSerializer(many=False)},
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(Email=email)
        except User.DoesNotExist:
            return Response(
                {"non_field_errors": ["Invalid email. User does not exist"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.check_password(password):
            try:
                # Try to get the existing token
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                # If the token doesn't exist, create it
                token = Token.objects.create(user=user)

            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"non_field_errors": ["Invalid password. Enter the correct password"]},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BookListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailsView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "BookID"


class BorrowedBooksListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BorrowedBooks.objects.all()
    serializer_class = BorrowedBooksSerializer


class BorrowedBooksDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BorrowedBooks.objects.all()
    serializer_class = BorrowedBooksSerializer
    lookup_field = "pk"
