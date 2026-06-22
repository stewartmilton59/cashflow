from django.db import models


from django.db import models

class Account(models.Model):
    # 1. Define the branch choices using TextChoices
    class BranchChoices(models.TextChoices):
        MAIN = 'MAIN', 'Main Branch'
        SWAHILI = 'SWAHILI', 'Swahili Branch'
        MULAGO = 'MULAGO', 'Mulago Branch'
        MSIMBAZI = 'MSIMBAZI', 'Msimbazi Branch'
        BIGONE = 'BIGONE', 'Big One Branch'
        GONGOLAMBOTO = 'GONGOLAMBOTO', 'Gongo La Mboto Branch'

    image = models.ImageField(upload_to='account_images/', null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)
    
    # 2. Add the choices attribute and set a default if desired
    branch = models.CharField(
        max_length=12, # Adjusted max_length to fit the longest database value ('MSIMBAZI', 'MULAGO', etc.)
        choices=BranchChoices.choices,
        default=BranchChoices.MAIN,
    )
    
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name