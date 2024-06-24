from flask import Flask, request, jsonify
from models import target_session, EncryptedData
from encryption import encrypt_data

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Encryption Service API. Use /encrypt and /decrypt endpoints."

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json['data']
    encrypted_data = encrypt_data(data)
    # Store encrypted data to database
    new_data = EncryptedData(data=encrypted_data)
    target_session.add(new_data)
    target_session.commit()
    return jsonify({'encrypted_data': encrypted_data})

# @app.route('/decrypt', methods=['POST'])
# def decrypt():
#     encrypted_data = request.json['encrypted_data']
#     data_type = request.json['data_type']
#     decrypted_data = decrypt_data(encrypted_data, data_type)
#     return jsonify({'decrypted_data': decrypted_data})

if __name__ == '__main__':
    app.run(debug=True)
