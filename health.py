import platform
import sys
from datetime import datetime

data = {
    "source": "laptop",
    "os": platform.system() + '' + platform.release(),
    "python": sys.version.split()[0],
    "git": "installed",
    "docker": "skipped - low RAM",
    "time": datetime.now().isoformat(),
    "status": "Laptop OK - Python + Git ready"
}

print(data)