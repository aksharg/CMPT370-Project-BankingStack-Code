import json
import mimetypes
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class serverDataStore:
    def __init__(self, server_params):
        self.server_params = server_params
        self.plaid_response = None

class plaidHTTPServer(BaseHTTPRequestHandler):
    def __init__(self, server_params: serverDataStore, *args, **kwargs):
        self.server_params = server_params
        super().__init__( *args, **kwargs)

    def fileServe(self, file_path):
        mime = mimetypes.guess_type(file_path)
        self.send_response(200)
        self.send_header('Content-type', mime[0])
        self.end_headers()

        with open(file_path, 'r') as f:
            html = f.read()

        html = html.replace('{{SERVER_PARAMS}}',json.dumps(self.server_params.server_params))
        self.wfile.write(html.encode('utf-8'))
        self.wfile.flush()

    def send404Error(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'not found')
        self.wfile.flush()

    def do_POST(self):
        path = self.path.split('?')[0]
        
        if path == '/api/success':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            self.server_params.plaid_response = json.loads(body)
            self.server.shutdown()
            self.server.server_close()
            return

        else:
            self.send404Error()

    def do_GET(self):
        path = self.path.split('?')[0]

        if path == '/link.html':
            self.fileServe('html\\link.html')
            return

        else:
            self.send404Error()

    def log_message(self, format, *args):
        pass

def openWebpage(url):
    webbrowser.open(url)

def startServer(env: str, client_name: str, token: str, page_title: str, account_name: str, type: str):
    """[summary]

    Args:
        env (str): [description]
        clientName (str): [description]
        token (str): [description]
        pageTitle (str): [description]
        accountName (str): [description]
        type (str): [description]

    Returns:
        [type]: [description]
    """

    server_params = dict(
        env=env,
        clientName=client_name,
        token=token,
        pageTitle=page_title,
        accountName=account_name,
        type=type
    )

    params = serverDataStore(server_params)

    def make_handler(*args, **kwargs):
        return plaidHTTPServer(params, *args, **kwargs)

    with ThreadingHTTPServer(('127.0.0.1', 8000), make_handler) as httpd:
        host, port = httpd.socket.getsockname()

        openWebpage(f'http://{host}:{port}/link.html')

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Keyboard interrupt, exiting Server.')
            sys.exit(0)

    
    return params.plaid_response

if __name__ == '__main__':
    startServer({})
    # startServer('a','b','c','d','e','f')