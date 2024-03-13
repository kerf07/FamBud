//Раздел расстановки соответствия между категориями транзакций и категорий бюджета
import React, { useState, useEffect } from 'react';
import { Table } from 'react-bootstrap';
import axios from 'axios';

const MappingPage = () => {
    const [budgetNames, setBudgetNames] = useState([]);
    const [categoryNames, setCategoryNames] = useState([]);

    useEffect(() => {
        // Функция для получения всех имен из модели Budget
        const fetchBudgetNames = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/budget/');
                setBudgetNames(response.data);
            } catch (error) {
                console.error('Ошибка получения имен из модели Budgets:', error);
            }
        };

        // Функция для получения всех имен из модели Categories
        const fetchCategoryNames = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/categories/');
                setCategoryNames(response.data);
            } catch (error) {
                console.error('Ошибка получения имен из модели Categories:', error);
            }
        };

        fetchBudgetNames();
        fetchCategoryNames();
    }, []);

    // Функция для установки соответствия между значениями из моделей Budget и Categories
    const handleMapping = async (categoryName, budgetName) => {
        // Ваша логика для установки соответствия
        const data = {
            budgetName: budgetName,
            categoryName: categoryName
        };
        try {
            const response = await axios.post('http://localhost:8000/api/update_category_budget/', data);
            console.log(`Соответствие ${budgetName} и ${categoryName} установлено`);
        } catch (error) {
            console.error('Ошибка установления соответствия:', error);
        }
    };

    return (
        <div>
            <div>
                <h2>Установить соответствие</h2>
                    <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>Категория</th>
                        <th>Бюджет</th>
                    </tr>
                    </thead>
                    <tbody>
                {categoryNames.map((categoryName, index) => (
                        <tr key={index}>
                            <td>{categoryName.name}</td>
                            <td>
                                <select onChange={(e) => handleMapping(categoryName.name, e.target.value)}>
                                <option value="">Выберите значение бюджета</option>
                                {budgetNames.map((budgetName, index) => (
                                    <option selected={categoryName.budget_id === budgetName.id} key={index} value={budgetName.name}>{budgetName.name}</option>
                                ))}
                                </select>
                            </td>
                        </tr>
                ))}
                    </tbody>
                    </Table>
            </div>
        </div>
    );
};

export default MappingPage;
