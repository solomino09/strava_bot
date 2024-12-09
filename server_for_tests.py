# import http.server
# import asyncio
#
#
# class RedirectHandler(http.server.BaseHTTPRequestHandler):
#     def __init__(self, handle_authorization_response, *args, **kwargs):
#         self.handle_authorization_response = handle_authorization_response
#         super().__init__(*args, **kwargs)
#
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#         self.wfile.write(b"<html><body><h1>Authorization successful \
#         </h1></body></html>")
#         asyncio.create_task(self.handle_authorization_response(self.path))
#
# def start(handle_code_callback, host: str="localhost", port: int=3000):
#     server_address = (host, port)
#     httpd = http.server.HTTPServer(
#         server_address,
#         lambda *args, **kwargs: RedirectHandler(handle_code_callback, \
#          *args, **kwargs),
#     )
#     httpd.handle_request()
#
#
# def stop(httpd):
#     if httpd:
#         httpd.shutdown()
#         print("Server stopped.")
import http.server
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread

class SimpleServer:
    # def __init__(self, host="localhost", port=8080):
    #     self.server_address = (host, port)
    #     self.httpd = http.server.HTTPServer(self.server_address, http.server.SimpleHTTPRequestHandler)
    #
    # # def start(self):
    # #     self.thread = Thread(target=self.httpd.serve_forever, daemon=True)
    # #     self.thread.start()
    # def start(self, http_server_instance=None):
    #     if http_server_instance is None:
    #         http_server_instance = self.httpd
    #     http_server_instance.serve_forever()
    #
    # # def stop(self):
    # #     self.httpd.shutdown()
    # #     self.httpd.server_close()
    # #     self.thread.join()
    # def stop(self):
    #     print("Stopping server...")
    #     if self.httpd:
    #         self.httpd.shutdown()
    #         self.httpd.server_close()
    #         print("Server stopped.")
    def __init__(self, host="localhost", port=0):  # Використовуємо порт 0 для автоматичного вибору доступного порту
        self.server_address = (host, port)
        self.httpd = http.server.HTTPServer(self.server_address, http.server.SimpleHTTPRequestHandler)
        self.httpd.timeout = 1
        self.running = False

    def start(self):
        self.thread = threading.Thread(target=self._run_server)
        self.thread.start()

    def _run_server(self):
        self.running = True
        self.httpd.handle_request()  # Обробляємо один запит
        self.running = False

    def stop(self):
        if self.running:
            self.httpd.shutdown()
            self.thread.join()
