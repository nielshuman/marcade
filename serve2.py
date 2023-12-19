from flask import Flask, send_from_directory
from waitress import serve

class DingesServer():
    def __init__(self, directory):
        self.app = Flask(__name__)
        self.directory = directory
        @self.app.route('/')
        def index():
            return serve_static('index.html')
        
        @self.app.route('/<path:filename>')
        def serve_static(filename):
            response = send_from_directory(self.directory, filename)
            response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
            response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'

            # voor de leuk nog wat headers
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
    
    def serve(self, port):
        serve(self.app, port=port)
    

if __name__ == '__main__':
    s = DingesServer('gunwizard')
    s.serve(8007)
    