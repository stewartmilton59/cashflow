from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User model with role-based access control."""
    class RoleChoices(models.TextChoices):
        DIRECTOR = 'DIRECTOR', 'Director'
        ACCOUNTANT = 'ACCOUNTANT', 'Accountant'

    role = models.CharField(
        max_length=12,
        choices=RoleChoices.choices,
        default=RoleChoices.ACCOUNTANT,
    )

    def is_director(self):
        return self.role == self.RoleChoices.DIRECTOR

    def is_accountant(self):
        return self.role == self.RoleChoices.ACCOUNTANT

    class Meta:
        db_table = 'auth_user'


class Account(models.Model):
    """Account/Staff profile linked to a User."""
    class BranchChoices(models.TextChoices):
        MAIN = 'MAIN', 'Main Branch'
        SWAHILI = 'SWAHILI', 'Swahili Branch'
        MULAGO = 'MULAGO', 'Mulago Branch'
        MSIMBAZI = 'MSIMBAZI', 'Msimbazi Branch'
        BIGONE = 'BIGONE', 'Big One Branch'
        GONGOLAMBOTO = 'GONGOLAMBOTO', 'Gongo La Mboto Branch'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='account_profile'
    )
    image = models.ImageField(upload_to='account_images/', null=True, blank=True)
    name = models.CharField(max_length=255)
    branch = models.CharField(
        max_length=12,
        choices=BranchChoices.choices,
        default=BranchChoices.MAIN,
    )
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        unique_together = ['user', 'branch']

    def __str__(self):
        return f"{self.name} ({self.get_branch_display()})"