import time
import requests
import threading
import signal
import sys
import urllib3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from prometheus_client import (
    CollectorRegistry,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)


URLS = ["https://httpstat.us/503", "https://httpstat.us/200"]

# Create Prometheus metrics
registry = CollectorRegistry()
url_up = Gauge(
    "sample_external_url_up",
    "URL availability (1=up, 0=down)",
    ["url"],
    registry=registry,
)
url_response_ms = Gauge(
    "sample_external_url_response_ms",
    "URL response time in milliseconds",
    ["url"],
    registry=registry,
)


# Check URLs and update metrics
def check_urls():
    for url in URLS:
        start = time.time()
        try:
            response = requests.get(url, timeout=3, verify=False)
            elapsed = (time.time() - start) * 1000
            url_up.labels(url=url).set(1 if response.status_code == 200 else 0)
            url_response_ms.labels(url=url).set(elapsed)
        except requests.RequestException:
            url_up.labels(url=url).set(0)
            url_response_ms.labels(url=url).set(0)


# Run URL checker in a background thread
def start_url_checker(interval=10):
    def loop():
        while True:
            check_urls()
            time.sleep(interval)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()


# HTTP handler
class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            check_urls()
            self.send_response(200)
            self.send_header("Content-Type", CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(generate_latest(registry))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


# Graceful shutdown support
def run():
    server_address = ("0.0.0.0", 8000)
    httpd = ThreadingHTTPServer(server_address, MetricsHandler)

    def shutdown_handler(signum, frame):
        print("\nShutting down server...")
        threading.Thread(target=httpd.shutdown).start()

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    print("Server is running at http://localhost:8000/metrics")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    run()
