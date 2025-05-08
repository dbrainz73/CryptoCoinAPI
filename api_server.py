from flask import Flask, request, jsonify
from crypto_coin import Blockchain, Transaction
from wallet_utils import create_wallet

app = Flask(__name__)

coin = Blockchain()
miner_private, miner_public = create_wallet()

@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    private, public = create_wallet()
    return jsonify({'private_key': private, 'public_key': public})

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(k in tx_data for k in required):
        return 'Missing transaction fields', 400
    transaction = Transaction(
        tx_data['sender'],
        tx_data['recipient'],
        tx_data['amount'],
        tx_data['signature']
    )
    try:
        coin.add_transaction(transaction)
        return 'Transaction added', 201
    except Exception as e:
        return str(e), 400

@app.route('/mine', methods=['GET'])
def mine():
    coin.mine_pending_transactions(miner_public)
    return jsonify({'message': 'Block mined successfully', 'miner': miner_public})

@app.route('/chain', methods=['GET'])
def full_chain():
    chain_data = []
    for block in coin.chain:
        chain_data.append({
            'timestamp': block.timestamp,
            'transactions': [tx.__dict__ for tx in block.transactions],
            'previous_hash': block.previous_hash,
            'nonce': block.nonce,
            'hash': block.hash
        })
    return jsonify({'chain': chain_data, 'length': len(chain_data)})

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = coin.get_balance(address)
    return jsonify({'balance': balance})

@app.route('/validate', methods=['GET'])
def validate():
    valid = coin.is_chain_valid()
    return jsonify({'valid': valid})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
