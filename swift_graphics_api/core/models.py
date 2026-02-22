from django.db import models
from django.conf import settings

class Service(models.Model):
    SERVICE_CHOICES = [
        ('business_card', 'Business Card Printing'),
        ('eulogy', 'Eulogy Writing & Printing'),
        ('general_printing', 'General Printing'),
        ('photocopy', 'Photocopy'),
        ('banner', 'Banner Printing'),
        ('other', 'Other Cyber Solutions'),
    ]

    name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    description = models.TextField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_type}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-calculate total price
        self.total_price = self.service.price_per_unit * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} by {self.customer} - {self.service.name}"


class BusinessCardDesign(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='business_card_design'
    )
    full_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='business_cards/logos/', blank=True, null=True)

    def __str__(self):
        return f"Business Card for {self.full_name}"


class EulogyDocument(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='eulogy_document'
    )
    deceased_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    date_of_death = models.DateField()
    eulogy_text = models.TextField()
    photo = models.ImageField(upload_to='eulogies/photos/', blank=True, null=True)
    number_of_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Eulogy for {self.deceased_name}"
