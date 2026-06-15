from flask import Flask, jsonify, request, render_template_string
import datetime

app = Flask(__name__)
latest_data = {"status": "waiting for laptop..."}

HTML = """
<!doctype html>
<html>
<head><title>Brick 1 Dashboard</title>
<style>
body{font-family:'Segoe UI';background:#0f172a;color:#e2e8f0;text-align:center;padding:40px}
.card{background:#1e293b;border-radius:16px;padding:30px;margin:20px auto;max-width:450px;box-shadow:0 10px 30px rgba(0,0,0,0.3)}
.bar{height:24px;background:#334155;border-radius:12px;overflow:hidden;margin:15px 0}
.fill{height:100%;background:linear-gradient(90deg,#22c55e,#16a34a);transition:width 0.5s}
.warn{background:linear-gradient(90deg,#f59e0b,#d97706)}
.danger{background:linear-gradient(90deg,#ef4444,#dc2626)}
h1{color:#38bdf8;font-size:28px}
h2{margin:5px 0;font-size:20px}
p{color:#94a3b8;font-size:14px}
</style>
</head>
<body>
<h1>🚀 Brick 1 Monitor</h1>
<div class="card">
<h2>CPU: {{cpu}}%</h2><div class="bar"><div class="fill {{'danger' if cpu>80 else 'warn' if cpu>60 else ''}}" style="width:{{cpu}}%"></div></div>
<h2>RAM: {{ram}}%</h2><div class="bar"><div class="fill {{'danger' if ram>80 else 'warn' if ram>60 else ''}}" style="width:{{ram}}%"></div></div>
<h2>Disk C: {{disk}}%</h2><div class="bar"><div class="fill {{'danger' if disk>80 else 'warn' if disk>60 else ''}}" style="width:{{disk}}%"></div></div>
<h2>Uptime: {{uptime}} hours</h2>
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
        uptime=d.get('uptime_hours',0),
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
