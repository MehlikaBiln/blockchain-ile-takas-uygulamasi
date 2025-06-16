from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL bağlantı adresi (kendine göre düzenle!)
DATABASE_URL = "postgresql://postgres:Mehli.8900@localhost:5432/takasdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency (FastAPI için)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
