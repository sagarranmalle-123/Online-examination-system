import os
import sys

# Add project root directory to sys.path so root-level modules (app, models, config) resolve cleanly
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Expose WSGI application instance for Vercel Serverless Functions
from app import app

# Provide standard aliases for serverless WSGI runners
handler = app
application = app
