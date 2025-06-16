from sqlalchemy import func
from models import Transaction ,User,Settings
from datetime import datetime

def validate_transaction(sender_email, receiver_email, item, db):
    if sender_email == receiver_email:
        return False, "Kendine takas gönderemezsin."

    receiver_user = db.query(User).filter(User.email == receiver_email).first()
    if not receiver_user:
        return False, "Alıcı sistemde kayıtlı değil."


    today = datetime.utcnow().date()
    transaction_count = db.query(Transaction).filter(
        Transaction.sender == sender_email,
        func.date(Transaction.timestamp) == today
    ).count()

    if transaction_count >= 3:
        return False, "Günlük işlem sınırına ulaşıldı."

    allowed_items = ["kitap", "oyuncak", "gıda", "ev eşyası", "elektronik"]
    if item.lower() not in allowed_items:
        return False, f"'{item}' geçerli bir ürün kategorisi değil."

    setting = db.query(Settings).first()
    if setting and setting.only_same_neighborhood:
        sender = db.query(User).filter(User.email == sender_email).first()
        receiver = db.query(User).filter(User.email == receiver_email).first()

        if not sender or not receiver:
            return False, "Kullanıcı bulunamadı."

        if sender.city != receiver.city or sender.neighborhood != receiver.neighborhood:
            return False, "Sadece aynı mahalledeki kullanıcılarla takas yapılabilir."


    return True, "İşlem geçerli"

