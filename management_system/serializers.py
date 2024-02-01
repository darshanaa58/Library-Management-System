# serializers.py

from rest_framework import serializers
from .models import User, Book, BookDetails, BorrowedBooks
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["UserID", "Name", "Email", "MembershipDate", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(Email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"non_field_errors": ["Invalid email. User does not exist"]}
            )

        if user.check_password(password):
            return user
        else:
            raise serializers.ValidationError(
                {"non_field_errors": ["Invalid password. Enter Correct password"]}
            )


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()


class BookDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetails
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    details = BookDetailsSerializer(required=False)

    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):
        details_data = validated_data.pop("details", None)
        book = Book.objects.create(**validated_data)
        if details_data:
            details_instance = BookDetails.objects.create(book=book, **details_data)
            # Set the 'details' field in the Book instance
            book.details = details_instance
            book.save()
        return book

    def update(self, instance, validated_data):
        # Update Book instance
        instance.Title = validated_data.get("Title", instance.Title)
        instance.ISBN = validated_data.get("ISBN", instance.ISBN)
        instance.PublishedDate = validated_data.get(
            "PublishedDate", instance.PublishedDate
        )
        instance.Genre = validated_data.get("Genre", instance.Genre)
        instance.save()

        # Update associated BookDetails instance
        details_data = validated_data.get("details")
        if details_data:
            details_instance = instance.details
            if details_instance:
                details_instance.NumberOfPages = details_data.get(
                    "NumberOfPages", details_instance.NumberOfPages
                )
                details_instance.Publisher = details_data.get(
                    "Publisher", details_instance.Publisher
                )
                details_instance.Language = details_data.get(
                    "Language", details_instance.Language
                )
                details_instance.save()
            else:
                details_instance = BookDetails.objects.create(
                    book=instance, **details_data
                )
                instance.details = details_instance
                instance.save()

        return instance


class BorrowedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBooks
        fields = "__all__"

    def update(self, instance, validated_data):
        # Check if ReturnDate is being updated
        return_date = validated_data.get("ReturnDate", instance.ReturnDate)

        # Update the instance
        instance.UserID = validated_data.get("UserID", instance.UserID)
        instance.BookID = validated_data.get("BookID", instance.BookID)
        instance.BorrowDate = validated_data.get("BorrowDate", instance.BorrowDate)
        instance.ReturnDate = return_date

        # Update the availability status of the associated book
        if return_date:
            instance.BookID.available = True  # Book is returned, set available to True
        else:
            instance.BookID.available = (
                False  # Book is borrowed, set available to False
            )

        # Save the changes to the book and the borrowed book
        instance.BookID.save()
        instance.save()

        return instance
