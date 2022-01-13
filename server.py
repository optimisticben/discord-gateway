from gevent.pywsgi import WSGIServer
from app import app
import os

DISCORD_CATCHA_PORT = 5000

if os.environ.get('DISCORD_CATCHA_PORT') != "":
    DISCORD_CATCHA_PORT = os.environ.get('DISCORD_CATCHA_PORT')

print(f"Serving on port {DISCORD_CATCHA_PORT}")

http_server = WSGIServer(('', int(DISCORD_CATCHA_PORT)), app)
http_server.serve_forever()