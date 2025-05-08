
# CryptoCoin API

This project simulates a basic cryptocurrency system with:

- Wallet creation using ECDSA keys
- Transaction signing and verification
- Blockchain with Proof-of-Work mining
- Flask REST API to interact with the system

## Endpoints

- `GET /wallet/new`: Create a new wallet (public/private key pair)
- `POST /transaction/new`: Submit a signed transaction
- `GET /mine`: Mine pending transactions into a new block
- `GET /chain`: View the full blockchain
- `GET /balance/<address>`: Check the balance of a wallet
- `GET /validate`: Validate blockchain integrity

## Setup

1. Install dependencies:
   ```bash
   pip install flask ecdsa
   ```

2. Run the server:
   ```bash
   python api_server.py
   ```

3. Use Postman or curl to interact with the API.
