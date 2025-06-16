import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import MakeTrade from './pages/takasGonder';
import TradeHistory from './pages/gecmisTakas';
import AdminPanel from './pages/adminpanel'


function Sidebar({ user, onLogout }) {
  const navigate = useNavigate();
  return (
    <div className="sidebar">
      <h2>📦 Menü</h2>
      <ul>
        <li onClick={() => navigate('/')}>🏠 Ana Sayfa</li>
        <li onClick={() => navigate('/profile')}>🧑 Profil</li>
        <li onClick={() => navigate('/trade')}>🔄 Takas Yap</li>
        <li onClick={() => navigate('/history')}>🕓 Geçmiş</li>
        {user?.role === 'admin' && (
          <li onClick={() => navigate('/admin')}>🛠 Admin Panel</li>
        )}
        <li onClick={onLogout}>🚪 Çıkış Yap</li>
      </ul>
    </div>
  );
}

function Home() {
  return (
    <div className="home">
      <div className="slider">
        <h2>🎁 Fazlalıklarını Takas Et!</h2>
        <p>İhtiyacın olmayanı ver, ihtiyacın olanı al.</p>
      </div>
      <div className="callout">
        ♻️ Takas, sürdürülebilir bir gelecek için önemli!
      </div>
    </div>
  );
}

function App() {
  const [token, setToken] = useState('');
  const [user, setUser] = useState(null);
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [registerForm, setRegisterForm] = useState({ name: '', email: '', password: '', city: '', neighborhood: '' });
  const [view, setView] = useState('login');

  useEffect(() => {
    if (token) {
      axios.get('http://localhost:8000/me', {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => setUser(res.data));
    }
  }, [token]);

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://localhost:8000/login', loginForm);
      setToken(res.data.access_token);
      localStorage.setItem('token', res.data.access_token); // 👈 BU SATIR ÖNEMLİ
      setView('main');
    } catch (err) {
      alert('Giriş başarısız');
    }
  };

  const handleRegister = async () => {
    try {
      await axios.post('http://localhost:8000/register', registerForm);
      alert('Kayıt başarılı. Şimdi giriş yapabilirsin.');
      setView('login');
    } catch (err) {
      alert('Kayıt başarısız');
    }
  };

  const handleLogout = () => {
    setToken('');
    setUser(null);
    setView('login');
  };

  if (view === 'login') {
    return (
      <div className="App">
        <h1 className="title">📦 Mahalle Takas Sistemi</h1>
        <div className="card">
          <h2>🔐 Giriş Yap</h2>
          <input placeholder="E-posta" onChange={e => setLoginForm({ ...loginForm, email: e.target.value })} />
          <input placeholder="Şifre" type="password" onChange={e => setLoginForm({ ...loginForm, password: e.target.value })} />
          <button onClick={handleLogin}>Giriş Yap</button>
          <p onClick={() => setView('register')}>Hesabın yok mu? Kayıt ol</p>
        </div>
      </div>
    );
  }

  if (view === 'register') {
    return (
      <div className="App">
        <h1 className="title">📦 Mahalle Takas Sistemi</h1>
        <div className="card">
          <h2>📝 Kayıt Ol</h2>
          <input placeholder="Ad" onChange={e => setRegisterForm({ ...registerForm, name: e.target.value })} />
          <input placeholder="E-posta" onChange={e => setRegisterForm({ ...registerForm, email: e.target.value })} />
          <input placeholder="Şifre" type="password" onChange={e => setRegisterForm({ ...registerForm, password: e.target.value })} />
          <input placeholder="Şehir" onChange={e => setRegisterForm({ ...registerForm, city: e.target.value })} />
          <input placeholder="Mahalle" onChange={e => setRegisterForm({ ...registerForm, neighborhood: e.target.value })} />
          <button onClick={handleRegister}>Kayıt Ol</button>
          <p onClick={() => setView('login')}>Zaten hesabım var</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="layout">
        <Sidebar user={user} onLogout={handleLogout} />
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/profile" element={<p>🧑 Profil Bilgileri Sayfası</p>} />
            <Route path="/trade" element={<MakeTrade />} />
            <Route path="/history" element={<TradeHistory />} />
            <Route path="/admin" element={user?.role === 'admin' ? <AdminPanel /> : <p>Erişim Yok</p>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
