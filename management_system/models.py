# models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, membership_date, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(
            email=email, name=name, membership_date=membership_date, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, name, membership_date, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, name, membership_date, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    MembershipDate = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        related_name="user_groups",  # Add a unique related_name
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        related_name="user_permissions",  # Add a unique related_name
    )

    USERNAME_FIELD = "Email"
    REQUIRED_FIELDS = ["Name", "MembershipDate"]

    def __str__(self):
        return self.Name


class BookDetails(models.Model):
    DetailsID = models.AutoField(primary_key=True)
    NumberOfPages = models.PositiveIntegerField()
    Publisher = models.CharField(max_length=255)
    Language = models.CharField(max_length=50)

    def __str__(self):
        return f"Details - {self.DetailsID}"


class Book(models.Model):
    BookID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=13, unique=True)
    PublishedDate = models.DateField()
    Genre = models.CharField(max_length=50)
    details = models.OneToOneField(
        BookDetails,
        on_delete=models.CASCADE,
        related_name="book",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Book - {self.Title}"


class BorrowedBooks(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    BookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    BorrowDate = models.DateField()
    ReturnDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.UserID.Name} - {self.BookID.Title}"

    def save(self, *args, **kwargs):
        # Check if ReturnDate is provided and is earlier than BorrowDate
        if self.ReturnDate and self.ReturnDate < self.BorrowDate:
            raise ValidationError("ReturnDate cannot be earlier than BorrowDate")

        super().save(*args, **kwargs)
