#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPT 转 AI 文本 —— exe 启动器

为什么要起一个本地 http 服务而不是直接把 HTML 塞进窗口：
  · DecompressionStream / 剪贴板 API 只在「安全上下文」里可用，
    localhost 算安全上下文，file:// 和 about:blank 不算。
  · 起在 127.0.0.1 的随机端口上，只监听本机，不对外暴露。
"""
import http.server
import os
import socket
import socketserver
import sys
import threading
import webbrowser

APP_NAME = "PPT 转 AI 文本"


def resource_path(rel: str) -> str:
    """兼容 PyInstaller 打包后的资源路径。"""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


def load_html() -> bytes:
    with open(resource_path("PPT转AI文本.html"), "rb") as f:
        return f.read()


HTML = load_html()


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(HTML)))
        # 明确不缓存，换版本后不会拿到旧页面
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(HTML)

    def log_message(self, *args):
        pass  # 静音，否则 --noconsole 下会往 stderr 抛


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def main():
    port = free_port()
    httpd = socketserver.TCPServer(("127.0.0.1", port), Handler)
    httpd.allow_reuse_address = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/"

    # 优先开原生窗口（WebView2，Win11 自带）；失败就退回默认浏览器
    try:
        import webview  # pywebview
        webview.create_window(APP_NAME, url, width=1120, height=880)
        webview.start()
    except Exception:
        webbrowser.open(url)
        # 浏览器模式下进程必须活着，否则服务就断了
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            pass
    finally:
        httpd.shutdown()


if __name__ == "__main__":
    main()
