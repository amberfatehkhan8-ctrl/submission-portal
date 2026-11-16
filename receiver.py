import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/report":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return
        with open("test-report.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Report received and saved ->", data.get("overall_status"))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"saved")


if __name__ == "__main__":
    print("Receiver listening on http://localhost:9000/report")
    HTTPServer(("0.0.0.0", 9000), Handler).serve_forever()