//Раздел загрузки файла с транзакциями
import React, { useState } from 'react';
import {Container, Table } from 'react-bootstrap';
import axios from 'axios';

const ImportPage = () => {
    const [transactions, setTransactions] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [numAddedRecords, setNumAddedRecords] = useState(null);

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('file', file);
        setIsLoading(true);
        try {
          const response = await axios.post('http://localhost:8000/api/upload/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
          setTransactions(response.data.transactions);
          setNumAddedRecords(response.data.num_added_records);
        } catch (error) {
          console.error('Error uploading file: ', error);
        } finally {
          setIsLoading(false);
        }
    };

    return (
      <Container>
        <input type="file" accept=".xls,.xlsx" onChange={handleFileUpload} disabled={isLoading}/>
        {isLoading ? 'Loading...' : 'Fetch Data'}
        {error && <div>Error: {error.message}</div>}
        <div>
          {numAddedRecords !== null && <p>Количество добавленных записей: {numAddedRecords}</p>}
        </div>
        <Table striped bordered hover>
          <thead>
          <tr>
            <th>Дата операции</th>
            <th>Дата платежа</th>
            <th>Номер карты</th>
            <th>Статус</th>
            <th>Сумма операции</th>
            <th>Валюта операции</th>
            <th>Сумма платежа</th>
            <th>Валюта платежа</th>
            <th>Кэшбэк</th>
            <th>Категория</th>
            <th>MCC</th>
            <th>Описание</th>
            <th>Бонусы (включая кэшбэк)</th>
            <th>Округление на инвесткопилку</th>
            <th>Сумма операции с округлением</th>
          </tr>
          </thead>
          <tbody>
          {transactions.map((transaction, index) => (
              <tr key={index}>
                <td>{transaction.date_of_operation}</td>
                <td>{transaction.date_of_payment}</td>
                <td>{transaction.card_number}</td>
                <td>{transaction.status}</td>
                <td>{transaction.operation_amount}</td>
                <td>{transaction.operation_currency}</td>
                <td>{transaction.payment_amount}</td>
                <td>{transaction.payment_currency}</td>
                <td>{transaction.cashback}</td>
                <td>{transaction.category}</td>
                <td>{transaction.mcc}</td>
                <td>{transaction.description}</td>
                <td>{transaction.bonuses}</td>
                <td>{transaction.rounding_for_savings}</td>
                <td>{transaction.operation_amount_rounded}</td>
              </tr>
          ))}
          </tbody>
        </Table>
      </Container>
    );
}

export default ImportPage;