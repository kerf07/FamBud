from rest_framework import serializers
from .models import Transaction, Categories, Budgets


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class BudgetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budgets
        fields = '__all__'