from django.contrib import admin
from .models import (
    Athlete, BillingPlan, AthleteSubscription, Payment,
    InvoiceTemplate, Invoice, EmailSettings, Workout, WorkoutCompletion
)


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'contact_number', 'created_at']
    search_fields = ['name', 'email', 'contact_number']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'email', 'contact_number', 'address')
        }),
        ('Profile', {
            'fields': ('profile', 'goals', 'fitness_evaluation')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BillingPlan)
class BillingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'service_level', 'billing_period', 'hsn_sac', 'base_price', 'is_active']
    list_filter = ['plan_type', 'service_level', 'billing_period', 'is_active']
    search_fields = ['name', 'hsn_sac']
    readonly_fields = ['hsn_sac', 'created_at', 'updated_at']
    fieldsets = (
        ('Plan Details', {
            'fields': ('name', 'plan_type', 'service_level', 'billing_period', 'hsn_sac')
        }),
        ('Pricing', {
            'fields': ('base_price', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AthleteSubscription)
class AthleteSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['athlete', 'billing_plan', 'final_price', 'start_date', 'end_date', 'status']
    list_filter = ['status', 'start_date', 'billing_plan']
    search_fields = ['athlete__name', 'billing_plan__name']
    readonly_fields = ['final_price', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Subscription', {
            'fields': ('athlete', 'billing_plan', 'start_date', 'end_date', 'status')
        }),
        ('Pricing & Discounts', {
            'fields': ('custom_discount_percent', 'custom_discount_amount', 'final_price')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['subscription', 'amount', 'due_date', 'payment_date', 'status', 'months_covered']
    list_filter = ['status', 'payment_method', 'due_date']
    search_fields = ['subscription__athlete__name', 'transaction_id', 'months_covered']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'due_date'
    fieldsets = (
        ('Payment Details', {
            'fields': ('subscription', 'amount', 'months_covered')
        }),
        ('Dates', {
            'fields': ('due_date', 'payment_date')
        }),
        ('Status & Method', {
            'fields': ('status', 'payment_method', 'transaction_id')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_paid']
    
    def mark_as_paid(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='PAID', payment_date=timezone.now().date())
        self.message_user(request, f'{updated} payment(s) marked as paid.')
    mark_as_paid.short_description = "Mark selected payments as paid"


@admin.register(InvoiceTemplate)
class InvoiceTemplateAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_gstin', 'company_pan', 'is_default']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'company_address', 'company_email', 'company_phone', 'company_website')
        }),
        ('Tax Information', {
            'fields': ('company_gstin', 'company_pan', 'include_gst', 'gst_rate')
        }),
        ('Bank Details', {
            'fields': ('bank_name', 'bank_account_number', 'bank_ifsc', 'bank_account_holder', 'bank_upi_id')
        }),
        ('Invoice Content', {
            'fields': ('terms_and_conditions', 'footer_note')
        }),
        ('Settings', {
            'fields': ('is_default',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer_name', 'invoice_date', 'total_amount', 'status']
    list_filter = ['status', 'invoice_date']
    search_fields = ['invoice_number', 'customer_name', 'customer_email']
    readonly_fields = ['invoice_number', 'pdf_generated_at', 'emailed_at', 'created_at', 'updated_at']
    date_hierarchy = 'invoice_date'
    fieldsets = (
        ('Invoice Details', {
            'fields': ('payment', 'template', 'invoice_number', 'invoice_date', 'due_date', 'status')
        }),
        ('Company Details', {
            'fields': ('company_name', 'company_address', 'company_gstin', 'company_pan', 'company_email', 'company_phone'),
            'classes': ('collapse',)
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'customer_address')
        }),
        ('Line Items', {
            'fields': ('line_items',)
        }),
        ('Amounts', {
            'fields': (
                'subtotal', 'discount_percent', 'discount_amount', 'taxable_amount',
                'cgst_rate', 'cgst_amount', 'sgst_rate', 'sgst_amount', 'igst_rate', 'igst_amount',
                'total_amount', 'amount_in_words'
            )
        }),
        ('Payment Terms', {
            'fields': ('payment_terms',)
        }),
        ('PDF & Email', {
            'fields': ('pdf_file', 'pdf_generated_at', 'emailed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ['provider', 'from_email', 'from_name', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Provider', {
            'fields': ('provider', 'is_active')
        }),
        ('SMTP Configuration', {
            'fields': ('smtp_host', 'smtp_port', 'smtp_use_tls', 'smtp_username', 'smtp_password')
        }),
        ('From Address', {
            'fields': ('from_email', 'from_name')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['athlete', 'date', 'workout_type', 'title', 'status']
    list_filter = ['status', 'workout_type', 'date']
    search_fields = ['athlete__name', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    fieldsets = (
        ('Workout Details', {
            'fields': ('athlete', 'date', 'workout_type', 'title', 'description')
        }),
        ('Targets', {
            'fields': ('target_distance', 'target_duration', 'target_tss')
        }),
        ('Status', {
            'fields': ('status', 'original_date')
        }),
        ('Coach Notes', {
            'fields': ('coach_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WorkoutCompletion)
class WorkoutCompletionAdmin(admin.ModelAdmin):
    list_display = ['workout', 'completion_quality', 'actual_date', 'reviewed_at']
    list_filter = ['completion_quality', 'actual_date']
    search_fields = ['workout__athlete__name', 'workout__title', 'athlete_comments']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Workout', {
            'fields': ('workout',)
        }),
        ('Completion Details', {
            'fields': ('athlete_link', 'actual_date', 'completion_quality')
        }),
        ('Actuals', {
            'fields': ('actual_distance', 'actual_duration', 'actual_tss')
        }),
        ('Comments & Feedback', {
            'fields': ('athlete_comments', 'coach_feedback', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
