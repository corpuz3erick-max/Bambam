
import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.transactions}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class BambamChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 50

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block of Bambam")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, miner_address):
        block = Block(
            len(self.chain),
            self.get_latest_block().hash,
            time.time(),
            self.pending_transactions
        )
        block.mine_block(self.difficulty)
        self.chain.append(block)
        
        self.pending_transactions = []
        self.pending_transactions.append({"sender": "NETWORK", "recipient": miner_address, "amount": self.mining_reward})

    def create_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({"sender": sender, "recipient": recipient, "amount": amount})

    def get_balance_of_address(self, address):
        balance = 0
        for block in self.chain:
            if isinstance(block.transactions, list):
                for trans in block.transactions:
                    if isinstance(trans, dict):
                        if trans["sender"] == address:
                            balance -= trans["amount"]
                        if trans["recipient"] == address:
                            balance += trans["amount"]
        return balance

# --- SETTING UP YOUR CUSTOM BAMBAM ECONOMY ---
bambam = BambamChain()

# Add transactions including your own wallet
bambam.create_transaction("Creator", "Erick", 500)
bambam.create_transaction("Creator", "Alice", 200)
bambam.create_transaction("Creator", "Bob", 150)
bambam.mine_pending_transactions("Miner_Dave")

# More trading
bambam.create_transaction("Erick", "Bob", 100)
bambam.create_transaction("Alice", "Charlie", 50)
bambam.mine_pending_transactions("Miner_Dave")

# --- CHECK BALANCES ---
print("--- FINAL BAMBAM WALLET BALANCES ---")
print(f"Erick: {bambam.get_balance_of_address('Erick')} BAM")
print(f"Alice: {bambam.get_balance_of_address('Alice')} BAM")
print(f"Bob: {bambam.get_balance_of_address('Bob')} BAM")
print(f"Charlie: {bambam.get_balance_of_address('Charlie')} BAM")
print(f"Miner Dave: {bambam.get_balance_of_address('Miner_Dave')} BAM")

# --- INSPECT THE BLOCKCHAIN HASHES ---
print("\n--- BLOCKCHAIN LEDGER & HASHES ---")
for block in bambam.chain:
    print(f"Block Index: {block.index}")
    print(f"Transactions: {block.transactions}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Block Hash: {block.hash}")
    print("-" * 30)
