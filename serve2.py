from flask import Flask, send_from_directory, redirect
from multiprocessing import Process
from flask_socketio import SocketIO
import eventlet
from eventlet import wsgi
from waitress import serve
eventlet.monkey_patch()
import os

class DingesServer():
    def __init__(self, directory, port, socketio=False, waitress=False):
        if socketio and waitress:
            raise Exception('Cant use socketio with waitress')
        self.waitress = waitress
        self.port = port
        self.app = Flask(__name__)
        self.directory = directory
        self.url = f'http://localhost:{port}/'
        if socketio:
            self.socketio = SocketIO(self.app)
        else:
            self.socketio = None

        @self.app.route('/', defaults={'path': ''})
        @self.app.route('/<path:path>') 
        def serve_static(path=''): 
            if path == 'socket.js':
                return send_from_directory('lib', 'socket.js')
            if os.path.isdir(os.path.join(self.directory, path)):
                if not path.endswith('/') and path != '':
                    return redirect(path + '/')
                path = os.path.join(path, 'index.html')
            
            response = send_from_directory(self.directory, path)
            response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
            response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'

            if path.endswith('.html'): inject_socketio(response)

            # nog wat headers voor de leuk
            # response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
            # response.headers['Pragma'] = 'no-cache'
            # response.headers['Expires'] = '0'
            return response
        
    def serve(self):
        print(f'Serving {self.directory} on {self.url}')
        if self.socketio:
            self.socketio.run(self.app, port=self.port)
        elif self.waitress:
            serve(self.app, port=self.port)
        else:
            wsgi.server(eventlet.listen(('', self.port)), self.app, log_output=False)
    
    def start(self):
        self.process = Process(target=self.serve)
        self.process.start()
        
    def stop(self):
        self.process.terminate()
        self.process.join()

    def wait(self):
        print(f'Waiting for {self.directory}...')
        self.process.join()

def inject_socketio(response):
    response.direct_passthrough = False
    injected_html = '<script src="/socket.js" crossorigin="anonymous"></script>'
    response.set_data(response.get_data().replace(b'</head>', f'{injected_html}</head>'.encode()))