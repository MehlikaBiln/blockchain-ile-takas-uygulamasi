from fastapi import APIRouter
from blockchain_instance import blockchain
from chain_verification import is_chain_valid

router = APIRouter(prefix="/verify", tags=["Chain Verification"])

@router.get("/chain")
def verify_chain():
    is_valid = is_chain_valid(blockchain.chain)
    return {"valid": is_valid, "message": "Zincir geçerli." if is_valid else "Zincirde bozulma var!"}