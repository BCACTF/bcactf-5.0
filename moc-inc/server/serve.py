from waitress import serve
from app import app

serve(app, listen='0.0.0.0:3000')
