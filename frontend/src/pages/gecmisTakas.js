import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TradeHistory() {
  const [transactions, setTransactions] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const res = await axios.get('http://localhost:8000/transactions/history', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setTransactions(res.data.history || []);
      } catch (err) {
        console.error('Geçmiş yüklenemedi:', err);
      }
    };

    fetchTransactions();
  }, [token]);

  return (
    <div className="card">
      <h2>🕓 Geçmiş Takaslar</h2>
      {transactions.length === 0 ? (
        <p>Henüz takas geçmişin yok.</p>
      ) : (
        <ul style={{ textAlign: 'left' }}>
          {transactions.map((tx, index) => (
            <li key={index}>
              <strong>{tx.receiver}</strong> ile <strong>{tx.item}</strong> takası yapıldı - <em>{tx.timestamp}</em>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default TradeHistory;