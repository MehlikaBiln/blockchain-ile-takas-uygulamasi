from pydantic import BaseModel

class TransactionInput(BaseModel):
    kiminle: str
    verilen_urun: str
    alinan_urun: str
