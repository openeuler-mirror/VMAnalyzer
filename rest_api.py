#!/usr/bin/env python3
"""
Simple REST API for VM metrics query
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import redis
import urllib.parse

API_PORT = 8080
r = redis.Redis()

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        if path == '/api/vms':
            # List all VMs
            keys = r.keys("vm:*")
            vms = [key.decode() for key in keys]
            response = {"vms": vms, "count": len(vms)}
        
        elif path.startswith('/api/vm/'):
            # Get specific VM metrics
            vm_uuid = path.split('/')[3]
            data = r.get(f"vm:{vm_uuid}")
            if data:
                response = {"vm_uuid": vm_uuid, "metrics": json.loads(data)}
            else:
                response = {"error": "VM not found"}
        
        elif path == '/api/health':
            # Health check
            response = {"status": "ok", "timestamp": time.time()}
        
        else:
            response = {"error": "Endpoint not found"}
        
        self.wfile.write(json.dumps(response, indent=2).encode())

def main():
    server = HTTPServer(('0.0.0.0', API_PORT), APIHandler)
    print(f"🚀 REST API running on port {API_PORT}")
    print(f"📋 Endpoints:")
    print(f"   GET /api/vms - List all VMs")
    print(f"   GET /api/vm/<uuid> - Get VM metrics")
    print(f"   GET /api/health - Health check")
    server.serve_forever()

if __name__ == "__main__":
    import time
    main()
