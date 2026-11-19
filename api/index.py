import os
import sys

# Add project root directory to sys.path so root-level modules (app, models, config) resolve cleanly
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Expose WSGI application instance for Vercel Serverless Functions
from app import app
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure reverse-proxy header handling for Vercel edge infrastructure
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Middleware to ensure PATH_INFO is cleanly routed even if prefixed by Vercel rewrite
class VercelPathFix:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        if path.startswith('/api/index'):
            stripped = path[len('/api/index'):]
            environ['PATH_INFO'] = stripped if stripped.startswith('/') else ('/' + stripped)
        elif path.startswith('/api'):
            stripped = path[len('/api'):]
            if stripped.startswith('/'):
                environ['PATH_INFO'] = stripped
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathFix(app.wsgi_app)

# Provide standard aliases for serverless WSGI runners
handler = app
application = app
