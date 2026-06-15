from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)
latest_data = {"status": "waiting for laptop..."}

@app.route('/health')
def health():
    return jsonify(latest_data)

@app.route('/update', methods=['POST'])
def update():
    global latest_data
    data = request.get_json()
    data['timestamp'] = datetime.datetime.now().isoformat()
    latest_data = data
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
