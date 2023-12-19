# #!/usr/bin/env python3
# from http.server import HTTPServer, SimpleHTTPRequestHandler, test
# import sys

# class Tyfusteringzooi (SimpleHTTPRequestHandler):
#     def end_headers (self):
#         self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
#         self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
#         SimpleHTTPRequestHandler.end_headers(self)

# if __name__ == '__main__':
#     test(Tyfusteringzooi, HTTPServer, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)

from http.server import HTTPServer, SimpleHTTPRequestHandler

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(CORSRequestHandler, self).end_headers()

class Kutserver():
    def __init__(self, port):
        self.httpd = HTTPServer(('localhost', port), CORSRequestHandler)
    def serve_forever(self):
        self.httpd.serve_forever()    

    def stop(self):
        self.httpd.shutdown()

# httpd = HTTPServer(('localhost', 8004), CORSRequestHandler)
# httpd.serve_forever()

if __name__ == '__main__':
    kutserver = Kutserver(8007)
    kutserver.serve_forever()