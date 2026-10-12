"""Double-click launcher: reuse a running Atelier or start the local server."""
import subprocess, sys, webbrowser
from pathlib import Path
from urllib.request import urlopen
URL='http://127.0.0.1:8768/'
try:
    response=urlopen(URL,timeout=1)
    if b'Quant Atelier' not in response.read(10000):
        raise RuntimeError('Port 8768 is occupied by another service. Use server.py --port with another port.')
    webbrowser.open(URL)
except (OSError,TimeoutError):
    child=subprocess.Popen([sys.executable,str(Path(__file__).with_name('server.py')),'--port','8768'])
    import time
    for _ in range(20):
        try:
            with urlopen(URL,timeout=.2) as response:
                if b'Quant Atelier' in response.read(10000):break
        except OSError:time.sleep(.1)
    else:
        print('Could not start Quant Atelier. Check the terminal output above.');sys.exit(1)
    webbrowser.open(URL)
    print('Leave this Terminal window open while practising. Ctrl+C stops the server.')
    try:child.wait()
    except KeyboardInterrupt:child.terminate();child.wait()
