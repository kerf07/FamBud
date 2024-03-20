from django.db import IntegrityError
from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Transaction, Budgets, Categories, Dictionary
from .serializers import TransactionSerializer, CategoriesSerializer, BudgetsSerializer
from datetime import datetime
# from decimal import Decimal
from django.core.exceptions import ValidationError
# import numpy as np
import pandas as pd


def parse_date2(x):
    if isinstance(x, float):
        return 0
    else:
        return datetime.strptime(str(x), '%d.%m.%Y').strftime('%Y-%m-%d')


class UploadFile(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        data = pd.read_excel(file)
        data['Дата операции'] = data['Дата операции'].apply(
            lambda x: datetime.strptime(x, '%d.%m.%Y %H:%M:%S'))
        data['Дата платежа'] = data['Дата платежа'].apply(parse_date2)
        data['Сумма операции'] = data['Сумма операции'].astype(str).str.replace(',', '.')
        data['Сумма платежа'] = data['Сумма платежа'].astype(str).str.replace(',', '.')
        data['Бонусы (включая кэшбэк)'] = data['Бонусы (включая кэшбэк)'].astype(str).str.replace(',', '.')
        data['Сумма операции с округлением'] = data['Сумма операции с округлением'].astype(str).str.replace(',', '.')
        for col in data.columns:
            if data[col].isnull().any():
                data.fillna({col: 0}, inplace=True)
                data.replace({col: 'NAN'}, {col: 0}, inplace=True)
        transactions = []
        for index, row in data.iterrows():
            try:
                if row['Дата платежа'] == 0:
                    pass
                else:
                    in_dictionary = False
                    try:
                        dictionary_obj = Dictionary.objects.get(cat_name_in_report=row['Категория'], descr_in_report=row['Описание'], mcc_in_report=row['MCC'])
                        in_dictionary = True
                    except Dictionary.DoesNotExist:
                        in_dictionary = False
                    transaction = Transaction(
                        date_of_operation=timezone.make_aware(row['Дата операции'], timezone.get_current_timezone()),
                        date_of_payment=row['Дата платежа'],
                        card_number=row['Номер карты'],
                        status=row['Статус'],
                        operation_amount=row['Сумма операции'].replace(',', '.'),
                        operation_currency=row['Валюта операции'],
                        payment_amount=row['Сумма платежа'].replace(',', '.'),
                        payment_currency=row['Валюта платежа'],
                        cashback=row['Кэшбэк'],
                        category=dictionary_obj.get_category_name() if in_dictionary and dictionary_obj.weight > 2 else row['Категория'],
                        mcc=row['MCC'],
                        description=row['Описание'],
                        bonuses=row['Бонусы (включая кэшбэк)'],
                        rounding_for_savings=row['Округление на инвесткопилку'],
                        operation_amount_rounded=row['Сумма операции с округлением'].replace(',', '.'),
                        suggested_category=dictionary_obj.get_category_name() if in_dictionary and dictionary_obj.weight < 3 else '',
                        original_category=row['Категория'] if in_dictionary and dictionary_obj.weight > 2 else ''
                    )
                    transaction.full_clean()
                    transactions.append(transaction)
            except ValidationError as e:
                print(f"Error processing row {index}: {e}")

        try:
            Transaction.objects.bulk_create(transactions)
        except IntegrityError as e:
            print(f"Error importing file: {e}")
        serializer = TransactionSerializer(transactions, many=True)
        num_added_records = len(transactions)
        return Response({'transactions': serializer.data, 'num_added_records': num_added_records})
        #return Response(serializer.data)

#Функция получения всех бюджетов
@api_view(['GET'])
def get_budget_names(request):
    #budget_names = Budgets.objects.values_list('name', flat=True)
    budgets = Budgets.objects.all()
    serializer = BudgetsSerializer(budgets, many=True)
    return Response(serializer.data)

#Функция получения всех категорий
@api_view(['GET'])
def get_category_names(request):
    categories = Categories.objects.all()
    #category_names = Categories.objects.values_list('name', flat=True)
    serializer = CategoriesSerializer(categories, many=True)
    return Response(serializer.data)

#Функция обновления соответствия категории бюджету
@api_view(['POST'])
def update_category_budget(request):
    if request.method == 'POST':
        budget_name = request.data.get('budgetName')
        category_name = request.data.get('categoryName')

        # Получаем объекты Budget и Categories по именам
        try:
            budget = get_object_or_404(Budgets, name=budget_name)
        except Budgets.DoesNotExist:
            return Response({'message': 'No MyModel matches the given query.'})
        category = get_object_or_404(Categories, name=category_name)

        # Обновляем значение budget_id_id в модели Categories
        category.budget_id_id = budget.id
        category.save()

        return Response({'message': 'Значение успешно обновлено'})
    else:
        return Response({'message': 'Неверный параметр запроса'})


