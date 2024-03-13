from django.db import models


# Create your models here.
class Transaction(models.Model):
    date_of_operation = models.DateField()
    date_of_payment = models.DateField(null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    operation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    operation_currency = models.CharField(max_length=3)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_currency = models.CharField(max_length=3, null=True, blank=True)
    cashback = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    mcc = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField()
    bonuses = models.DecimalField(max_digits=10, decimal_places=2)
    rounding_for_savings = models.DecimalField(max_digits=10, decimal_places=2)
    operation_amount_rounded = models.DecimalField(max_digits=10, decimal_places=2)
    suggested_category = models.CharField(max_length=100, null=True, blank=True)
    original_category = models.CharField(max_length=100, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['date_of_operation', 'operation_amount']

class Budgets(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

class Categories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    budget_id = models.ForeignKey(Budgets, null=True, on_delete=models.SET_NULL)

class Dictionary(models.Model):
    cat_name_in_report = models.CharField(max_length=100, null=True, blank=True)
    descr_in_report = models.CharField(max_length=100, null=True, blank=True)
    mcc_in_report = models.CharField(max_length=100, null=True, blank=True)
    category_id = models.ForeignKey(Categories, null=True, on_delete=models.SET_NULL)
    weight = models.DecimalField(max_digits=10, default=0, decimal_places=2)

    class Meta:
        unique_together = ['cat_name_in_report', 'descr_in_report', 'mcc_in_report']
