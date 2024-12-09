import http.server
import threading


class SimpleServer:
    def __init__(self, host="localhost", port=0):  # use port 0 to automatically select an available port
        self.server_address = (host, port)
        self.httpd = http.server.HTTPServer(self.server_address, http.server.SimpleHTTPRequestHandler)
        self.httpd.timeout = 1
        self.running = False

    def start(self):
        self.thread = threading.Thread(target=self._run_server)
        self.thread.start()

    def _run_server(self):
        self.running = True
        self.httpd.handle_request()
        self.running = False

    def stop(self):
        if self.running:
            self.httpd.shutdown()
            self.thread.join()
