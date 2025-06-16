import React, { useEffect, useState } from 'react';
import axios from 'axios';

function AdminPanel() {
  const token = localStorage.getItem('token');
  const [users, setUsers] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [chain, setChain] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const headers = { Authorization: `Bearer ${token}` };

        const usersRes = await axios.get('http://localhost:8000/settings/admin/users', { headers });
        setUsers(usersRes.data);

        const txRes = await axios.get('http://localhost:8000/settings/admin/transactions', { headers });
        setTransactions(txRes.data);

        const chainRes = await axios.get('http://localhost:8000/chain', { headers });
        setChain(chainRes.data.chain || []);

      } catch (err) {
        setError('Erişim reddedildi veya veriler alınamadı.');
      }
    };

    fetchData();
  }, [token]);

  if (error) return <p className="error">🚫 {error}</p>;

  return (
    <div className="card">
      <h2>🛠 Admin Paneli</h2>

      <h3>👥 Kullanıcılar</h3>
      <ul>
        {users.map((u) => (
          <li key={u.id}>
            {u.name} ({u.email}) - Rol: {u.role}
          </li>
        ))}
      </ul>

      <h3>🔄 Tüm Takaslar</h3>
      <ul>
        {transactions.map((t) => (
          <li key={t.id}>
            {t.sender} ↔ {t.receiver} | {t.item} | {new Date(t.timestamp).toLocaleString()}
          </li>
        ))}
      </ul>

      <h3>⛓️ Blok Zinciri</h3>
      <ul>
        {chain.map((block, idx) => (
          <li key={idx}>
            <strong>Blok {block.index}</strong> | Hash: {block.hash.slice(0, 16)}... | Tx Sayısı: {block.transactions.length}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AdminPanel;
