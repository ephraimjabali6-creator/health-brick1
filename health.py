from flask import Flask, jsonify
import platform, psutil, datetime

app = Flask(__name__)

@app.route('/health')
def health():
    data = {
        "device": platform.node(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "timestamp": datetime.datetime.now().isoformat()
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)