import hashlib
import json

# chain_verification.py içinde
def is_chain_valid(chain):
    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i - 1]

        if current_block.previous_hash != previous_block.hash:
            print(f"❌ Block {i}'in previous_hash uyuşmuyor.")
            return False

        block_dict = current_block.__dict__.copy()
        block_dict.pop("hash", None)
        calculated_hash = hashlib.sha256(json.dumps(block_dict, sort_keys=True).encode()).hexdigest()

        if current_block.hash != calculated_hash:
            print(f"❌ Block {i}'in hash değeri uyuşmuyor.")
            print("🔴 Orijinal  :", current_block.hash)
            print("🔁 Hesaplanan:", calculated_hash)
            print("📦 Veri:", json.dumps(block_dict, indent=2))
            return False

    return True
