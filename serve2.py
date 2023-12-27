from flask import Flask, send_from_directory
from multiprocessing import Process
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()

class DingesServer():
    def __init__(self, directory, port, socketio=False):
        self.port = port
        self.app = Flask(__name__)
        self.directory = directory
        self.url = f'http://localhost:{port}/'
        if socketio:
            self.socketio = SocketIO(self.app)
        else:
            self.socketio = None

        @self.app.route('/')
        def index():
            return serve_static('index.html')
        
        @self.app.route('/<path:filename>')
        def serve_static(filename):
            response = send_from_directory(self.directory, filename)
            response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
            response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'

            if filename.endswith('.html'): inject_socketio(response)

            # nog wat headers voor de leuk
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
    
    def serve(self):
        if self.socketio:
            self.socketio.run(self.app, port=self.port)
        else:
            eventlet.wsgi.server(eventlet.listen(('', self.port)), self.app)
    
    def start(self):
        self.process = Process(target=self.serve)
        self.process.start()
        
    def stop(self):
        self.process.terminate()
        self.process.join()

if __name__ == '__main__':
    s = DingesServer('gunwizard')
    s.start()

def inject_socketio(response):
    response.direct_passthrough = False
    injected_html = '''
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js" integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA==" crossorigin="anonymous"></script>
'''
    response.set_data(response.get_data().replace(b'</head>', f'{injected_html}</head>'.encode()))