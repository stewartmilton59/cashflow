from django.db import models


class Sale(models.Model):
    # Define text choices for the payment method badge logic
    class PaymentMethods(models.TextChoices):
        CASH = 'CASH', 'Cash'
        PHONE = 'PHONE', 'Phone Payment'

    # DecimalField prevents precision issues common with floating-point currency calculations
    amount = models.DecimalField(
        max_length=12, 
        max_digits=12, 
        decimal_places=2,
        help_text="Amount in Tanzanian Shillings (Tshs)"
    )
    
    payment_method = models.CharField(
        max_length=5,
        choices=PaymentMethods.choices,
        default=PaymentMethods.CASH
    )
    
    # auto_now_add automatically stamps the current system date and time when a sale is saved
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']  # Orders most recent sales first by default

    def __str__(self):
        return f"{self.get_payment_method_display()} - {self.amount} Tshs ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"