import hashlib
import json
from datetime import datetime
from models import BlockModel  # Veritabanı modeli

import json

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = json.loads(transactions) if isinstance(transactions, str) else transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": str(self.timestamp),  # 💡 güvenli string
            "transactions": self.transactions if isinstance(self.transactions, list) else json.loads(
                self.transactions),
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
            }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []

    def create_genesis_block(self):
        genesis_block = Block(0, datetime.utcnow().isoformat(), [], "0", 0)
        genesis_block.hash = self.proof_of_work(genesis_block)
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash()

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self, db):
        if not self.unconfirmed_transactions:
            print("No unconfirmed transactions.")
            return None

        last_block = self.last_block
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.unconfirmed_transactions,
            timestamp=datetime.utcnow().isoformat(),
            previous_hash=last_block.hash
        )

        print(f"Mining block {new_block.index}...")
        proof = self.proof_of_work(new_block)
        print(f"Proof found: {proof}")

        if not self.add_block(new_block, proof):
            return None

        block_entry = BlockModel(
            index=new_block.index,
            timestamp=datetime.utcnow(),
            transactions=json.dumps(new_block.transactions),
            previous_hash=new_block.previous_hash,
            hash=new_block.hash,
            nonce=new_block.nonce
        )

        try:
            db.add(block_entry)
            db.commit()
            print(f"Block {new_block.index} successfully added to the database.")
        except Exception as e:
            db.rollback()
            print(f"Error saving block to the database: {e}")

        self.unconfirmed_transactions = []
        return new_block.index

    def load_chain_from_db(self, db):
        print("Zincir veritabanından yükleniyor...")
        from models import BlockModel
        blocks = db.query(BlockModel).order_by(BlockModel.index).all()
        self.chain = []
        for b in blocks:
            block = Block(
                index=b.index,
                timestamp=b.timestamp.isoformat(),
                transactions=json.loads(b.transactions),
                previous_hash=b.previous_hash,
                nonce=b.nonce
            )
            block.hash = b.hash
            self.chain.append(block)
        if not self.chain:
            self.create_genesis_block()

