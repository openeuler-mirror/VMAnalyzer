#!/usr/bin/env python3
"""
Prometheus metrics exporter for VMAnalyzer
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import redis

METRICS_PORT = 9273
r = redis.Redis()

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4')
            self.end_headers()
            
            try:
                keys = r.keys("vm:*")
            except Exception:
                keys = []
            for key in keys:
                data = json.loads(r.get(key))
                vm_uuid = key.decode().replace(':', '_')
                
                # CPU metrics
                self.wfile.write(f'vm_cpu_usage{{vm="{vm_uuid}"}} {data.get("cpu_usage", 0)}\n'.encode())
                # Memory metrics
                self.wfile.write(f'vm_memory_usage{{vm="{vm_uuid}"}} {data.get("memory_usage", 0)}\n'.encode())
                # Disk metrics
                self.wfile.write(f'vm_disk_usage{{vm="{vm_uuid}"}} {data.get("disk_usage", 0)}\n'.encode())
            
        else:
            self.send_response(404)
            self.end_headers()

def main():
    server = HTTPServer(('0.0.0.0', METRICS_PORT), MetricsHandler)
    print(f"🚀 Prometheus exporter running on port {METRICS_PORT}")
    print(f"📊 Metrics endpoint: http://localhost:{METRICS_PORT}/metrics")
    server.serve_forever()

if __name__ == "__main__":
    main()
