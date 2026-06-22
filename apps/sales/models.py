from django.db import models
from django.conf import settings


class Sale(models.Model):
    """Sale model with branch tracking and payment method."""
    class PaymentMethods(models.TextChoices):
        CASH = 'CASH', 'Cash'
        PHONE = 'PHONE', 'Phone Payment'

    class BranchChoices(models.TextChoices):
        MAIN = 'MAIN', 'Main Branch'
        SWAHILI = 'SWAHILI', 'Swahili Branch'
        MULAGO = 'MULAGO', 'Mulago Branch'
        MSIMBAZI = 'MSIMBAZI', 'Msimbazi Branch'
        BIGONE = 'BIGONE', 'Big One Branch'
        GONGOLAMBOTO = 'GONGOLAMBOTO', 'Gongo La Mboto Branch'

    accountant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sales',
        help_text="The accountant who recorded this sale"
    )

    branch = models.CharField(
        max_length=12,
        choices=BranchChoices.choices,
        default=BranchChoices.MAIN,
        help_text="Branch where this sale was recorded"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Amount in Tanzanian Shillings (Tshs)"
    )

    payment_method = models.CharField(
        max_length=5,
        choices=PaymentMethods.choices,
        default=PaymentMethods.CASH
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional description or note"
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def __str__(self):
        return f"{self.get_branch_display()} - {self.get_payment_method_display()} - {self.amount} Tshs"