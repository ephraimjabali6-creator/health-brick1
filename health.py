from flask import Flask, jsonify, request, render_template_string
import datetime

app = Flask(__name__)
history = []  # stores last 100 readings
latest_data = {"status": "waiting for laptop..."}

HTML = """
<!doctype html>
<html>
<head><title>Brick 1 Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body{font-family:'Segoe UI';background:#0f172a;color:#e2e8f0;text-align:center;padding:20px}
.card{background:#1e293b;border-radius:16px;padding:25px;margin:20px auto;max-width:800px}
.bar{height:24px;background:#334155;border-radius:12px;overflow:hidden;margin:15px 0}
.fill{height:100%;background:linear-gradient(90deg,#22c55e,#16a34a)}
.warn{background:linear-gradient(90deg,#f59e0b,#d97706)}
.danger{background:linear-gradient(90deg,#ef4444,#dc2626)}
h1{color:#38bdf8}
canvas{background:#0f172a;border-radius:12px;padding:10px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:800px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<h1>🚀 Brick 1 Monitor - DESKTOP-VB07DH3</h1>

<div class="card">
<h2>Live Stats</h2>
<h3>CPU: {{cpu}}% | RAM: {{ram}}% | Disk: {{disk}}% | Up: {{uptime}}h</h3>
<div class="bar"><div class="fill {{'danger' if cpu>80 else 'warn' if cpu>60 else ''}}" style="width:{{cpu}}%"></div></div>
<div class="bar"><div class="fill {{'danger' if ram>80 else 'warn' if ram>60 else ''}}" style="width:{{ram}}%"></div></div>
<div class="bar"><div class="fill {{'danger' if disk>80 else 'warn' if disk>60 else ''}}" style="width:{{disk}}%"></div></div>
<p>Last update: {{time}}</p>
</div>

<div class="grid">
<div class="card"><canvas id="cpuChart"></canvas></div>
<div class="card"><canvas id="ramChart"></canvas></div>
</div>

<script>
const labels = {{labels|safe}};
new Chart(document.getElementById('cpuChart'), {
  type:'line', data:{labels:labels, datasets:[{label:'CPU %',data:{{cpu_data|safe}},borderColor:'#38bdf8',tension:0.3}]},
  options:{plugins:{legend:{labels:{color:'#e2e8f0'}}},scales:{x:{ticks:{color:'#94a3b8'}},y:{ticks:{color:'#94a3b8'}}}}
});
new Chart(document.getElementById('ramChart'), {
  type:'line', data:{labels:labels, datasets:[{label:'RAM %',data:{{ram_data|safe}},borderColor:'#22c55e',tension:0.3}]},
  options:{plugins:{legend:{labels:{color:'#e2e8f0'}}},scales:{x:{ticks:{color:'#94a3b8'}},y:{ticks:{color:'#94a3b8'}}}}
});
</script>
<meta http-equiv="refresh" content="30">
</body></html>
"""

@app.route('/')
def dashboard():
    d = latest_data
    labels = [h['timestamp'][11:16] for h in history[-24:]]  # last 24 readings = 24 min
    cpu_data = [h.get('cpu_percent',0) for h in history[-24:]]
    ram_data = [h.get('memory_percent',0) for h in history[-24:]]
    return render_template_string(HTML, 
        cpu=d.get('cpu_percent',0), ram=d.get('memory_percent',0), 
        disk=d.get('disk_percent',0), uptime=d.get('uptime_hours',0),
        time=d.get('timestamp','never'), labels=labels, 
        cpu_data=cpu_data, ram_data=ram_data)

@app.route('/health')
def health():
    return jsonify(latest_data)

@app.route('/update', methods=['POST'])
def update():
    global latest_data
    data = request.get_json()
    data['timestamp'] = datetime.datetime.now().isoformat()
    latest_data = data
    history.append(data)
    if len(history) > 100: history.pop(0)  # keep last 100
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
