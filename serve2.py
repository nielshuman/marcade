from flask import Flask, send_from_directory
from waitress import serve
from multiprocessing import Process

class DingesServer():
    def __init__(self, directory, port):
        self.port = port
        self.app = Flask(__name__)
        self.directory = directory
        self.url = f'http://localhost:{port}/'
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
    
    def serve(self):
        serve(self.app, port=self.port)
    
    def start(self):
        self.process = Process(target=self.serve)
        self.process.start()
        
    def stop(self):
        self.process.terminate()
        self.process.join()

if __name__ == '__main__':
    s = DingesServer('gunwizard')
    s.serve(8007)
    