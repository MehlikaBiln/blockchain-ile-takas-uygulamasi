from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models
from blockchain_instance import blockchain
from auth import router as auth_router, get_current_user
from chain_verification import is_chain_valid
from smart_contracts import validate_transaction
from database import get_db, SessionLocal
from routers.settings import router as settings_router
from routers.admin import router as admin_router
from Shemas import TransactionInput
from routers.transactions import router as transaction_router

# 🚀 FastAPI uygulaması
app = FastAPI()
router = APIRouter()

# ✅ CORS middleware (React frontend için zorunlu!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için açık bırakıldı, prod'da sınırlamalısın
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 🔗 Tüm router'lar bağlanıyor
app.include_router(auth_router)
app.include_router(settings_router)
app.include_router(transaction_router)
app.include_router(admin_router)
app.include_router(transaction_router)


# 🔄 Zinciri açılışta veritabanından yükle
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    blockchain.load_chain_from_db(db)
    db.close()

# ✅ Ana sayfa testi
@app.get("/")
def read_root():
    return {"message": "Blockchain Marketplace API çalışıyor."}


@router.post("/transactions/new")
def new_transaction(
    data: TransactionInput,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 💡 KURALLARI DOĞRULA
    is_valid, message = validate_transaction(
        sender_email=current_user.email,
        receiver_email=data.kiminle,  # isme göre kontrol ediyor
        item=data.verilen_urun,  # sadece verilen_urun kontrolü yeterli (kategoride var mı)
        db=db
    )

    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    # ✅ Blockchain’e ekle
    tx_data = {
        "kullanici": current_user.email,
        "kiminle": data.kiminle,
        "verilen_urun": data.verilen_urun,
        "alinan_urun": data.alinan_urun
    }
    blockchain.add_new_transaction(tx_data)

    db.commit()

    return {"message": "Takas işlemi kaydedildi. Zincire eklemek için ⛏️ madencilik yap!"}

app.include_router(router)
# ⛏ Madencilik (blok kazımı)
@app.get("/mine")
def mine_block(db: Session = Depends(get_db)):
    index = blockchain.mine(db)
    if index is not None:
        return {"message": f"Block {index} mined successfully"}
    return {"message": "No transactions to mine"}

# 🔗 Tüm zinciri getir
@app.get("/chain")
def full_chain():
    return {
        "length": len(blockchain.chain),
        "chain": [block.__dict__ for block in blockchain.chain]
    }

@router.get("/chain/verify")
def verify_chain():
    is_valid = is_chain_valid(blockchain.chain)
    return {"valid": is_valid}


from routers.verify import router as verify_router
app.include_router(verify_router)