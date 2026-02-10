from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from decimal import Decimal


class Athlete(models.Model):
    """Athlete profile linked to Django User for authentication"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='athlete_profile')
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number")]
    )
    address = models.TextField(help_text="Billing address for invoices")
    profile = models.TextField(blank=True, help_text="Bio, background, etc.")
    goals = models.TextField(blank=True, help_text="Athlete's goals")
    fitness_evaluation = models.TextField(blank=True, help_text="Initial fitness assessment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Sync email with User model
        if self.user:
            self.user.email = self.email
            self.user.save()
        super().save(*args, **kwargs)


class BillingPlan(models.Model):
    """Billing plans with auto-generated HSN/SAC codes"""
    
    PLAN_TYPE_CHOICES = [
        ('RUNNING', 'Running'),
        ('TRIATHLON', 'Triathlon'),
    ]
    
    SERVICE_LEVEL_CHOICES = [
        ('FOCUS', 'Focus'),
        ('PERSONAL', 'Personal'),
    ]
    
    BILLING_PERIOD_CHOICES = [
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
    ]
    
    name = models.CharField(max_length=200, help_text="e.g., Running Focus - Monthly")
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    service_level = models.CharField(max_length=20, choices=SERVICE_LEVEL_CHOICES)
    billing_period = models.CharField(max_length=20, choices=BILLING_PERIOD_CHOICES)
    hsn_sac = models.CharField(max_length=20, editable=False, help_text="Auto-generated HSN/SAC code")
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.TextField(help_text="Plan details and features")
    is_active = models.BooleanField(default=True, help_text="Available for new subscriptions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['plan_type', 'service_level', 'billing_period']
        unique_together = ['plan_type', 'service_level', 'billing_period']

    def __str__(self):
        return f"{self.name} (₹{self.base_price})"

    def save(self, *args, **kwargs):
        # Auto-generate HSN/SAC code
        prefix = "RUN" if self.plan_type == "RUNNING" else "TRI"
        level = "FOCUS" if self.service_level == "FOCUS" else "PERSONAL"
        period = "1MO" if self.billing_period == "MONTHLY" else "1QTR"
        self.hsn_sac = f"{prefix}{level}{period}"
        super().save(*args, **kwargs)


class AthleteSubscription(models.Model):
    """Athlete subscription to a billing plan with custom discounts"""
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAUSED', 'Paused'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='subscriptions')
    billing_plan = models.ForeignKey(BillingPlan, on_delete=models.PROTECT, related_name='subscriptions')
    custom_discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage discount (0-100)"
    )
    custom_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Flat discount amount"
    )
    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        help_text="Calculated: base_price - discounts"
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Null for ongoing subscriptions")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.athlete.name} - {self.billing_plan.name}"

    def save(self, *args, **kwargs):
        # Calculate final price
        base = self.billing_plan.base_price
        discount_pct = base * (self.custom_discount_percent / 100)
        self.final_price = base - discount_pct - self.custom_discount_amount
        
        # Ensure final price is not negative
        if self.final_price < 0:
            self.final_price = Decimal('0.00')
        
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Payment records for athlete subscriptions"""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('UPI', 'UPI'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('OTHER', 'Other'),
    ]
    
    subscription = models.ForeignKey(AthleteSubscription, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    transaction_id = models.CharField(max_length=200, blank=True, help_text="UPI transaction ID or reference")
    months_covered = models.CharField(max_length=100, help_text="e.g., 'February 2026' or 'Jan-Mar 2026'")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.subscription.athlete.name} - ₹{self.amount} ({self.status})"

    def is_overdue(self):
        """Check if payment is overdue"""
        if self.status == 'PENDING' and self.due_date:
            return timezone.now().date() > self.due_date
        return False


class InvoiceTemplate(models.Model):
    """Invoice template with company details and GST information"""
    
    company_name = models.CharField(max_length=200, default="TAILWIND")
    company_address = models.TextField()
    company_gstin = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', 
                                   message="Enter valid GSTIN format")],
        help_text="15-character GSTIN (optional)"
    )
    company_pan = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', 
                                   message="Enter valid PAN format")],
        help_text="10-character PAN (required)"
    )
    company_email = models.EmailField()
    company_phone = models.CharField(max_length=15)
    company_website = models.URLField(blank=True)
    bank_name = models.CharField(max_length=200, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_ifsc = models.CharField(
        max_length=11,
        blank=True,
        validators=[RegexValidator(regex=r'^[A-Z]{4}0[A-Z0-9]{6}$', 
                                   message="Enter valid IFSC code")]
    )
    bank_account_holder = models.CharField(max_length=200, blank=True)
    bank_upi_id = models.CharField(max_length=100, blank=True, help_text="e.g., mved@ybl")
    terms_and_conditions = models.TextField(blank=True)
    footer_note = models.TextField(default="Thank you for your business!")
    include_gst = models.BooleanField(default=True)
    gst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18.0,
        validators=[MinValueValidator(0), MaxValueValidator(28)]
    )
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} Template"

    def save(self, *args, **kwargs):
        # Ensure only one default template
        if self.is_default:
            InvoiceTemplate.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class Invoice(models.Model):
    """Generated invoice for payments"""
    
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='invoice')
    template = models.ForeignKey(InvoiceTemplate, on_delete=models.PROTECT)
    invoice_number = models.CharField(max_length=50, unique=True, editable=False)
    invoice_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    
    # Company details (snapshot from template)
    company_name = models.CharField(max_length=200)
    company_address = models.TextField()
    company_gstin = models.CharField(max_length=15, blank=True)
    company_pan = models.CharField(max_length=10)
    company_email = models.EmailField()
    company_phone = models.CharField(max_length=15)
    
    # Customer details
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    customer_address = models.TextField()
    
    # Line items (JSON)
    line_items = models.JSONField(help_text="Array of line items with description, hsn_sac, qty, rate, amount")
    
    # Amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    igst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    igst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_words = models.CharField(max_length=500)
    
    payment_terms = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    pdf_generated_at = models.DateTimeField(null=True, blank=True)
    emailed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-invoice_date']

    def __str__(self):
        return f"{self.invoice_number} - {self.customer_name}"

    def save(self, *args, **kwargs):
        # Auto-generate invoice number
        if not self.invoice_number:
            year = self.invoice_date.year
            month = self.invoice_date.month
            count = Invoice.objects.filter(
                invoice_date__year=year,
                invoice_date__month=month
            ).count() + 1
            self.invoice_number = f"INV-{year}-{month:02d}-{count:04d}"
        super().save(*args, **kwargs)


class EmailSettings(models.Model):
    """Email configuration (singleton)"""
    
    PROVIDER_CHOICES = [
        ('GMAIL', 'Gmail'),
        ('SMTP', 'SMTP'),
        ('SENDGRID', 'SendGrid'),
        ('MAILGUN', 'Mailgun'),
        ('SES', 'Amazon SES'),
        ('OTHER', 'Other'),
    ]
    
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='GMAIL')
    smtp_host = models.CharField(max_length=200, default='smtp.gmail.com')
    smtp_port = models.IntegerField(default=587)
    smtp_use_tls = models.BooleanField(default=True)
    smtp_username = models.CharField(max_length=200)
    smtp_password = models.CharField(max_length=200, help_text="App password for Gmail")
    from_email = models.EmailField(default='mehul@mehulved.com')
    from_name = models.CharField(max_length=200, default='TAILWIND Coaching')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Email Settings"

    def __str__(self):
        return f"Email Settings ({self.provider})"

    def save(self, *args, **kwargs):
        # Ensure only one active settings
        if self.is_active:
            EmailSettings.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class Workout(models.Model):
    """Workout assigned to athlete"""
    
    STATUS_CHOICES = [
        ('UPCOMING', 'Upcoming'),
        ('COMPLETED', 'Completed'),
        ('SKIPPED', 'Skipped'),
        ('RESCHEDULED', 'Rescheduled'),
    ]
    
    WORKOUT_TYPE_CHOICES = [
        ('EASY', 'Easy Run'),
        ('TEMPO', 'Tempo Run'),
        ('INTERVALS', 'Intervals'),
        ('LONG_RUN', 'Long Run'),
        ('RECOVERY', 'Recovery Run'),
        ('SPEED_WORK', 'Speed Work'),
        ('HILL_REPEATS', 'Hill Repeats'),
        ('FARTLEK', 'Fartlek'),
        ('BIKE', 'Bike'),
        ('SWIM', 'Swim'),
        ('BRICK', 'Brick Workout'),
        ('REST', 'Rest Day'),
        ('CROSS_TRAINING', 'Cross Training'),
    ]
    
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateField()
    workout_type = models.CharField(max_length=50, choices=WORKOUT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Workout plan details")
    target_distance = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="In kilometers")
    target_duration = models.IntegerField(null=True, blank=True, help_text="In minutes")
    target_tss = models.IntegerField(null=True, blank=True, help_text="Training Stress Score")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UPCOMING')
    original_date = models.DateField(null=True, blank=True, help_text="Original date if rescheduled")
    coach_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['athlete', 'date', 'workout_type']

    def __str__(self):
        return f"{self.athlete.name} - {self.title} ({self.date})"

    def is_overdue(self):
        """Check if workout is overdue (past date and not completed/skipped)"""
        if self.status == 'UPCOMING' and self.date:
            return timezone.now().date() > self.date
        return False


class WorkoutCompletion(models.Model):
    """Athlete's completion record for a workout"""
    
    COMPLETION_QUALITY_CHOICES = [
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('SATISFACTORY', 'Satisfactory'),
        ('STRUGGLED', 'Struggled'),
        ('INCOMPLETE', 'Incomplete'),
    ]
    
    workout = models.OneToOneField(Workout, on_delete=models.CASCADE, related_name='completion')
    athlete_link = models.URLField(blank=True, help_text="Strava/Garmin activity link")
    actual_distance = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    actual_duration = models.IntegerField(null=True, blank=True, help_text="In minutes")
    actual_tss = models.IntegerField(null=True, blank=True)
    completion_quality = models.CharField(max_length=20, choices=COMPLETION_QUALITY_CHOICES, default='INCOMPLETE')
    actual_date = models.DateField(null=True, blank=True)
    athlete_comments = models.TextField(blank=True)
    coach_feedback = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.workout.title} - {self.completion_quality}"

    def save(self, *args, **kwargs):
        # Update workout status based on completion
        if self.completion_quality != 'INCOMPLETE':
            self.workout.status = 'COMPLETED'
            self.workout.save()
        super().save(*args, **kwargs)

