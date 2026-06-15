from flask import Flask, jsonify, request, render_template_string
import datetime

app = Flask(__name__)
latest_data = {"status": "waiting for laptop..."}

HTML = """
<!doctype html>
<html>
<head><title>Brick 1 Dashboard</title>
<style>
body{font-family:Arial;background:#0f172a;color:#e2e8f0;text-align:center;padding:40px}
.card{background:#1e293b;border-radius:16px;padding:30px;margin:20px auto;max-width:400px}
.bar{height:20px;background:#334155;border-radius:10px;overflow:hidden;margin:10px 0}
.fill{height:100%;background:#22c55e}
.warn{background:#f59e0b}
.danger{background:#ef4444}
h1{color:#38bdf8}
</style>
</head>
<body>
<h1>🚀 Brick 1 - DESKTOP-VB07DH3</h1>
<div class="card">
<h2>CPU: {{cpu}}%</h2><div class="bar"><div class="fill" style="width:{{cpu}}%"></div></div>
<h2>RAM: {{ram}}%</h2><div class="bar"><div class="fill {{'danger' if ram>80 else 'warn' if ram>60 else ''}}" style="width:{{ram}}%"></div></div>
<h2>Disk C: {{disk}}%</h2><div class="bar"><div class="fill {{'danger' if disk>80 else 'warn' if disk>60 else ''}}" style="width:{{disk}}%"></div></div>
<p>Last update: {{time}}</p>
</div>
<meta http-equiv="refresh" content="10">
</body></html>
"""

@app.route('/')
def dashboard():
    d = latest_data
    return render_template_string(HTML, 
        cpu=d.get('cpu_percent',0), 
        ram=d.get('memory_percent',0), 
        disk=d.get('disk_percent',0),
        time=d.get('timestamp','never'))

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
