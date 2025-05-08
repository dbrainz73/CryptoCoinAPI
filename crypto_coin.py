
import hashlib
import json
import time
import ecdsa

class Transaction:
    def __init__(self, sender, recipient, amount, signature=""):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

    def sign_transaction(self, private_key):
        if self.sender == "SYSTEM":
            return
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
        self.signature = sk.sign(json.dumps(self.to_dict(), sort_keys=True).encode()).hex()

    def is_valid(self):
        if self.sender == "SYSTEM":
            return True
        if not self.signature:
            return False
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.sender), curve=ecdsa.SECP256k1)
        return vk.verify(bytes.fromhex(self.signature), json.dumps(self.to_dict(), sort_keys=True).encode())

class Block:
    def __init__(self, timestamp, transactions, previous_hash=""):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        tx_data = [tx.__dict__ for tx in self.transactions]
        block_string = json.dumps({
            'timestamp': self.timestamp,
            'transactions': tx_data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while not self.hash.startswith('0' * difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

    def has_valid_transactions(self):
        return all(tx.is_valid() for tx in self.transactions)

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 100

    def create_genesis_block(self):
        return Block(time.time(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, mining_reward_address):
        block = Block(time.time(), self.pending_transactions, self.get_latest_block().hash)
        block.mine_block(self.difficulty)

        self.chain.append(block)
        reward_tx = Transaction("SYSTEM", mining_reward_address, self.mining_reward)
        self.pending_transactions = [reward_tx]

    def add_transaction(self, transaction):
        if not transaction.sender or not transaction.recipient:
            raise Exception("Transaction must include sender and recipient")
        if not transaction.is_valid():
            raise Exception("Invalid transaction signature")
        self.pending_transactions.append(transaction)

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.recipient == address:
                    balance += tx.amount
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if not curr.has_valid_transactions():
                return False
            if curr.hash != curr.calculate_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True
