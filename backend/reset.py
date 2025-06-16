from database import Base, engine
import models

print("📛 Tüm tablolar siliniyor...")
Base.metadata.drop_all(bind=engine)

print("✅ Tablolar yeniden oluşturuluyor...")
Base.metadata.create_all(bind=engine)
