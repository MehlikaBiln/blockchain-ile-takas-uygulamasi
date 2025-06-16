# Mahalle Arası Takas Uygulaması

Bu proje, **React** ile geliştirilmiş ön yüz, **FastAPI** ile yazılmış arka yüz ve **PostgreSQL** veritabanı kullanan, blockchain teknolojisi ile desteklenen mahalle arası takas uygulamasıdır.

---

##  Proje Özellikleri

- Kullanıcılar mahallerindeki diğer kullanıcılarla güvenli şekilde takas yapabilir.
- Blockchain altyapısı ile takas işlemleri şeffaf ve değiştirilemez olarak saklanır.
- Kullanıcı kayıt, giriş ve takas işlemleri backend API ile yönetilir.
- PostgreSQL veritabanı ile kullanıcı ve takas bilgileri tutulur.
- React frontend, kullanıcı dostu ve modern bir arayüz sunar.

---

## Klasör Yapısı

takas/
├── frontend/ # React tabanlı ön yüz uygulaması
├── backend/ # FastAPI tabanlı arka yüz uygulaması
└── README.md # Proje açıklamaları

---

## Çalıştırma Talimatları

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows PowerShell için: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload

### Frontend (React)
cd frontend
npm install
npm start
