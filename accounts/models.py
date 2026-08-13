
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from academy.models import Academy


class Role(models.TextChoices):
    SUPERADMIN = "SUPERADMIN", "Super Admin"
    ADMIN = "ADMIN", "Academy Admin"
    COACH = "COACH", "Coach"
    GUARDIAN = "GUARDIAN", "Guardian"
    SCOUT = "SCOUT", "Scout"


class CustomUserManager(BaseUserManager):

    def create_user(
        self,
        username,
        email,
        password=None,
        role=None,
        **extra_fields
    ):

        if not email:
            raise ValueError("The Email field must be set")

        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            role=role,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(
        self,
        username,
        email,
        password=None,
        **extra_fields
    ):

        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_active"] = True

        return self.create_user(
            username=username,
            email=email,
            password=password,
            role=Role.SUPERADMIN,
            **extra_fields
        )


class User(AbstractUser):

    role = models.CharField(
        max_length=15,
        choices=Role.choices,
        default=Role.GUARDIAN
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    academy = models.ForeignKey(
        Academy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"


class AdminProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": Role.ADMIN},
        related_name="admin_profile"
    )

    fullname = models.CharField(max_length=255)

    def __str__(self):
        return self.fullname


class CoachProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": Role.COACH},
        related_name="coach_profile"
    )

    fullname = models.CharField(max_length=255)

    coach_id = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return f"Coach {self.fullname} ({self.coach_id})"


class GuardianProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": Role.GUARDIAN},
        related_name="guardian_profile"
    )

    fullname = models.CharField(max_length=255)

    player_code = models.CharField(
        max_length=50
    )

    def __str__(self):
        return f"Guardian {self.fullname} (Child Code: {self.player_code})"


class ScoutProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": Role.SCOUT},
        related_name="scout_profile"
    )

    fullname = models.CharField(max_length=255)

    region = models.CharField(
        max_length=100,
        help_text="Assigned country or region"
    )

    def __str__(self):
        return f"Scout {self.fullname} ({self.region})"

