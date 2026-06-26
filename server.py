"""Servidor local do sorteador."""

import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8501
ROOT = Path(__file__).resolve().parent


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    with ReusableTCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"Sorteador rodando em {url}")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")


if __name__ == "__main__":
    main()
