import sys
import os
import subprocess
import http.server
import socketserver
import threading
import shlex
import streamlit as st

UUID = st.secrets["UUID"]
NEZHA_SERVER = st.secrets["NEZHA_SERVER"]
NEZHA_KEY = st.secrets["NEZHA_KEY"]
ARGO_DOMAIN = st.secrets["ARGO_DOMAIN"]
ARGO_AUTH = st.secrets["ARGO_AUTH"]
NAME = st.secrets["NAME"]
CHAT_ID = st.secrets["CHAT_ID"]
BOT_TOKEN = st.secrets["BOT_TOKEN"]

PORT = int(os.environ.get('PORT') or 3000) # http port

class MyHandler(http.server.SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world')
        elif self.path == '/sub':
            try:
                with open("./sub.txt", 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Error reading file')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')
httpd = socketserver.TCPServer(('', PORT), MyHandler)
server_thread = threading.Thread(target=httpd.serve_forever)
server_thread.daemon = True
server_thread.start()

env_exports = " ".join([
    f'UUID={shlex.quote(UUID)}',
    f'NEZHA_SERVER={shlex.quote(NEZHA_SERVER)}',
    f'NEZHA_KEY={shlex.quote(NEZHA_KEY)}',
    f'ARGO_DOMAIN={shlex.quote(ARGO_DOMAIN)}',
    f'ARGO_AUTH={shlex.quote(ARGO_AUTH)}',
    f'NAME={shlex.quote(NAME)}',
    f'CHAT_ID={shlex.quote(CHAT_ID)}',
    f'BOT_TOKEN={shlex.quote(BOT_TOKEN)}'
])

shell_command = f"{env_exports} chmod +x start.sh && {env_exports} ./start.sh"

try:
    completed_process = subprocess.run(['bash', '-c', shell_command], stdout=sys.stdout, stderr=subprocess.PIPE, text=True, check=True)

    print("App is running")

except subprocess.CalledProcessError as e:
    print(f"Error: {e.returncode}")
    print("Standard Output:")
    print(e.stdout)
    print("Standard Error:")
    print(e.stderr)
    sys.exit(1)

server_thread.join()
