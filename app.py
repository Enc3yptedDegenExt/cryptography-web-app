from flask import Flask, render_template, request, jsonify
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/encrypt', methods=['POST'])
def encrypt_text():
    text = request.form.get('text')
    key = get_random_bytes(16) # AES-128
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
    iv = cipher.iv
    ct = iv + ct_bytes
    return jsonify({'ciphertext': ct.hex(), 'key': key.hex()})

@app.route('/decrypt', methods=['POST'])
def decrypt_text():
    ct_hex = request.form.get('ciphertext')
    key_hex = request.form.get('key')
    ct = bytes.fromhex(ct_hex)
    key = bytes.fromhex(key_hex)
    iv = ct[:16]
    ct_bytes = ct[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ct_bytes), AES.block_size).decode('utf-8')
    return jsonify({'plaintext': plaintext})

if __name__ == '__main__':
    app.run(debug=True)
