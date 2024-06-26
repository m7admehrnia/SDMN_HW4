import http.server
import socketserver
import json

PORT = 8000
status = {"status": "OK"}

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/v1/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status).encode())
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == '/api/v1/status':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_status = json.loads(post_data)
            status.update(new_status)
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status).encode())
        else:
            self.send_error(404, "Not Found")

handler = RequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)

print(f"Serving on port {PORT}")
httpd.serve_forever()
