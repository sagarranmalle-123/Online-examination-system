import os
import tempfile

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def get_db_uri():
    # Priority 1: Check environment variables for PostgreSQL / Cloud Database
    # Supports standard DATABASE_URL as well as Vercel Postgres defaults:
    # POSTGRES_URL, POSTGRES_URL_NON_POOLING, POSTGRES_PRISMA_URL.
    raw_url = (
        os.environ.get('DATABASE_URL') or 
        os.environ.get('POSTGRES_URL') or 
        os.environ.get('POSTGRES_URL_NON_POOLING') or
        os.environ.get('POSTGRES_PRISMA_URL') or
        ''
    ).strip()
    if raw_url:
        db_url = raw_url
        # Normalize legacy 'postgres://' URI scheme and ensure compatible SQLAlchemy 2.0 driver prefix
        if db_url.startswith('postgres://') or db_url.startswith('postgresql://'):
            try:
                import psycopg  # psycopg v3
                driver_prefix = 'postgresql+psycopg://'
            except ImportError:
                try:
                    import psycopg2  # psycopg2-binary
                    driver_prefix = 'postgresql+psycopg2://'
                except ImportError:
                    driver_prefix = 'postgresql://'

            if db_url.startswith('postgres://'):
                db_url = db_url.replace('postgres://', driver_prefix, 1)
            elif db_url.startswith('postgresql://') and '+' not in db_url.split('://')[0]:
                db_url = db_url.replace('postgresql://', driver_prefix, 1)
        return db_url

    # Priority 2: Local development with SQLite
    inst_dir = os.path.join(BASE_DIR, 'instance')
    try:
        os.makedirs(inst_dir, exist_ok=True)
        # Test if the directory is writable (not on a read-only serverless filesystem)
        test_file = os.path.join(inst_dir, '.write_test')
        with open(test_file, 'w') as f:
            f.write('ok')
        os.remove(test_file)
        return 'sqlite:///' + os.path.join(inst_dir, 'exam_system.db')
    except Exception:
        # Fallback for serverless environments with a read-only filesystem (e.g. Vercel)
        # when running without a remote DATABASE_URL configured
        temp_dir = tempfile.gettempdir()
        return 'sqlite:///' + os.path.join(temp_dir, 'exam_system.db')

class Config:
    SECRET_KEY = (
        os.environ.get('SECRET_KEY') or 
        os.environ.get('FLASK_SECRET_KEY') or 
        'presidency-university-cse2271-secret-key-2026'
    )
    SQLALCHEMY_DATABASE_URI = get_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('VERCEL') == '1' or os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() in ('true', '1')
