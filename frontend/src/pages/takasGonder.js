import React, { useState } from 'react';
import axios from 'axios';

function MakeTrade() {
  const [form, setForm] = useState({ kiminle: '', verilen_urun: '', alinan_urun: '' });
  const [message, setMessage] = useState('');
  const [blockVisible, setBlockVisible] = useState(false);
  const token = localStorage.getItem('token');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      const res = await axios.post('http://localhost:8000/transactions/new', form, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      setMessage(res.data.message || "İşlem başarılı.");
      setBlockVisible(true);
    } catch (err) {
      setMessage(err.response?.data?.detail || err.response?.data || 'İşlem başarısız.');
    }
  };

  const handleMine = async () => {
    try {
      const res = await axios.get('http://localhost:8000/mine', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMessage(res.data.message || "Blok oluşturuldu.");
      setBlockVisible(false);
    } catch (err) {
      setMessage('Blok oluşturulamadı.');
    }
  };

  return (
    <div className="card">
      <h2>🔄 Takas Yap</h2>
      <input name="kiminle" placeholder="Kiminle takas yaptın?" onChange={handleChange} value={form.kiminle} />
      <input name="verilen_urun" placeholder="Ne verdin?" onChange={handleChange} value={form.verilen_urun} />
      <input name="alinan_urun" placeholder="Ne aldın?" onChange={handleChange} value={form.alinan_urun} />
      <button onClick={handleSubmit}>İşlem Gönder</button>
      {blockVisible && <button onClick={handleMine}>⛏️ Blok Oluştur</button>}
      <p>{typeof message === 'string' ? message : JSON.stringify(message)}</p>
    </div>
  );
}

export default MakeTrade;
