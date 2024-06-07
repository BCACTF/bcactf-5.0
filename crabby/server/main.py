from flask import Flask, request, jsonify
import base64

app = Flask(__name__)
SECRET = base64.b64encode(b"some_super_secret_key_text_here")

FLAG = "bcactf{f4ke_flag}"

with open("../flag.txt", "r") as f:
    FLAG = f.read().strip()

@app.route('/flag', methods=['POST'])
def flag():
    data = request.headers.get("Authorization").encode()
    if data == SECRET:
        return jsonify({"flag": f"{FLAG}"})
    return jsonify({"error": "Unauthorized"}), 401
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7787)