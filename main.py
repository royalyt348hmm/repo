#!/usr/bin/env python3
"""
Web-based Terminal using xterm.js and aiohttp.
Run with: python main.py [port]
"""

import os
import sys
import pty
import struct
import fcntl
import termios
import signal
import asyncio
import logging
from aiohttp import web

# ========== কনফিগারেশন ==========
DEFAULT_PORT = 8080
SHELL = os.environ.get('SHELL', '/bin/bash')
WS_PATH = '/ws'

# লগিং সেটআপ (ঐচ্ছিক)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('webterm')

# ========== টার্মিনাল হ্যান্ডলার ==========
class TerminalSession:
    """একটি PTY সেশন পরিচালনা করে এবং WebSocket-এর সাথে সংযোগ রাখে"""
    def __init__(self, websocket):
        self.websocket = websocket
        self.pid = None
        self.master_fd = None
        self.loop = asyncio.get_running_loop()

    async def start(self):
        """PTY সেশন শুরু করুন এবং I/O হ্যান্ডলিং সেট করুন"""
        try:
            # PTY ফর্ক করুন
            self.pid, self.master_fd = pty.fork()
            if self.pid == 0:  # চাইল্ড প্রক্রিয়া
                # শেল চালু করুন
                os.execvp(SHELL, [SHELL, '--login'])
            else:
                # প্যারেন্ট: master_fd নন-ব্লকিং করুন
                fl = fcntl.fcntl(self.master_fd, fcntl.F_GETFL)
                fcntl.fcntl(self.master_fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

                # master_fd থেকে পড়ার জন্য ইভেন্ট লুপে যোগ করুন
                self.loop.add_reader(self.master_fd, self._on_pty_output)

                # WebSocket থেকে বার্তা প্রক্রিয়া করুন
                async for msg in self.websocket:
                    if msg.type == web.WSMsgType.TEXT:
                        self._on_ws_message(msg.data)
                    elif msg.type == web.WSMsgType.BINARY:
                        self._on_ws_message(msg.data)
                    elif msg.type == web.WSMsgType.ERROR:
                        logger.error('WebSocket error')
                        break

        except Exception as e:
            logger.exception('Terminal start failed')
            await self.cleanup()
            raise

    def _on_pty_output(self):
        """PTY master_fd থেকে ডাটা পড়ে WebSocket-এ পাঠায়"""
        try:
            data = os.read(self.master_fd, 1024)
            if data:
                asyncio.create_task(self.websocket.send_bytes(data))
            else:
                # PTY বন্ধ হয়ে গেছে
                asyncio.create_task(self.cleanup())
        except OSError as e:
            if e.errno != 11:  # EAGAIN ইগনোর করুন
                logger.error(f'PTY read error: {e}')
                asyncio.create_task(self.cleanup())

    def _on_ws_message(self, data):
        """WebSocket থেকে পাওয়া ডাটা PTY-তে লিখুন"""
        try:
            if isinstance(data, str):
                data = data.encode()
            os.write(self.master_fd, data)
        except Exception as e:
            logger.error(f'Write error: {e}')

    def resize(self, cols, rows):
        """টার্মিনালের উইন্ডো সাইজ পরিবর্তন করুন"""
        try:
            winsize = struct.pack('HHHH', rows, cols, 0, 0)
            fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, winsize)
        except Exception as e:
            logger.error(f'Resize failed: {e}')

    async def cleanup(self):
        """PTY ও চাইল্ড প্রক্রিয়া পরিষ্কার করুন"""
        if self.master_fd is not None:
            self.loop.remove_reader(self.master_fd)
            os.close(self.master_fd)
        if self.pid:
            try:
                os.kill(self.pid, signal.SIGTERM)
                await asyncio.sleep(0.1)
                os.waitpid(self.pid, os.WNOHANG)
            except ProcessLookupError:
                pass
        await self.websocket.close()

# ========== ওয়েব হ্যান্ডলার ==========
async def websocket_handler(request):
    """WebSocket সংযোগ হ্যান্ডল করুন"""
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    session = TerminalSession(ws)
    try:
        await session.start()
    except asyncio.CancelledError:
        pass
    finally:
        await session.cleanup()
    return ws

async def index_handler(request):
    """মূল HTML পৃষ্ঠা পরিবেশন করুন"""
    return web.Response(text=HTML_PAGE, content_type='text/html')

# ========== HTML পৃষ্ঠা (xterm.js) ==========
HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Web Terminal - Full Access</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm/css/xterm.css" />
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #1e1e2f;
            display: flex;
            flex-direction: column;
            height: 100vh;
            font-family: 'Fira Code', monospace;
        }
        #terminal-container {
            flex: 1;
            padding: 10px;
        }
        .status-bar {
            background: #2d2d3a;
            color: #ccc;
            padding: 6px 12px;
            font-size: 13px;
            border-top: 1px solid #3a3a4a;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status-bar a {
            color: #9cdcfe;
            text-decoration: none;
        }
        .status-bar a:hover {
            text-decoration: underline;
        }
        .fullscreen-btn {
            background: none;
            border: none;
            color: #ccc;
            cursor: pointer;
            font-size: 16px;
        }
        .fullscreen-btn:hover {
            color: white;
        }
    </style>
</head>
<body>
    <div id="terminal-container"></div>
    <div class="status-bar">
        <span>⚡ WebTerm v1.0 | Connected to <strong>${SHELL}</strong></span>
        <div>
            <button class="fullscreen-btn" id="fullscreen">⛶ Fullscreen</button>
            <span> | </span>
            <a href="#" id="reconnect">⟳ Reconnect</a>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/xterm/lib/xterm.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/xterm-addon-fit/lib/xterm-addon-fit.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/xterm-addon-web-links/lib/xterm-addon-web-links.js"></script>
    <script>
        const term = new Terminal({
            cursorBlink: true,
            theme: {
                background: '#1e1e2f',
                foreground: '#d4d4d4',
                cursor: '#aeafad',
                selectionBackground: '#3a3a4a'
            },
            fontSize: 14,
            fontFamily: 'monospace, "Fira Code", "Courier New"'
        });
        const fitAddon = new FitAddon.FitAddon();
        term.loadAddon(fitAddon);
        term.loadAddon(new WebLinksAddon.WebLinksAddon());

        let socket = null;
        let reconnectAttempts = 0;

        function connect() {
            const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${location.host}/ws`;
            socket = new WebSocket(wsUrl);
            socket.binaryType = 'arraybuffer';

            socket.onopen = () => {
                console.log('WebSocket connected');
                reconnectAttempts = 0;
                term.clear();
                fitAddon.fit();
                // initial resize
                sendResize();
            };

            socket.onmessage = (event) => {
                if (event.data instanceof ArrayBuffer) {
                    const data = new Uint8Array(event.data);
                    term.write(data);
                } else {
                    term.write(event.data);
                }
            };

            socket.onclose = () => {
                console.log('WebSocket disconnected');
                term.write('\\r\\n\\x1b[31m[Disconnected]\\x1b[0m\\r\\n');
                // auto reconnect after 2 seconds
                setTimeout(() => {
                    if (reconnectAttempts < 5) {
                        reconnectAttempts++;
                        connect();
                    } else {
                        term.write('\\r\\n\\x1b[31mFailed to reconnect. Please refresh the page.\\x1b[0m\\r\\n');
                    }
                }, 2000);
            };

            socket.onerror = (err) => {
                console.error('WebSocket error:', err);
            };
        }

        function sendResize() {
            if (socket && socket.readyState === WebSocket.OPEN) {
                const { cols, rows } = term;
                const resizeMsg = JSON.stringify({ resize: { cols, rows } });
                socket.send(resizeMsg);
            }
        }

        // terminal input -> WebSocket
        term.onData(data => {
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(data);
            }
        });

        // window resize handler
        window.addEventListener('resize', () => {
            fitAddon.fit();
            sendResize();
        });

        // fullscreen toggle
        const fullscreenBtn = document.getElementById('fullscreen');
        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
                fullscreenBtn.textContent = '✕ Exit';
            } else {
                document.exitFullscreen();
                fullscreenBtn.textContent = '⛶ Fullscreen';
            }
        }
        fullscreenBtn.addEventListener('click', toggleFullscreen);
        document.addEventListener('fullscreenchange', () => {
            if (document.fullscreenElement) {
                fullscreenBtn.textContent = '✕ Exit';
            } else {
                fullscreenBtn.textContent = '⛶ Fullscreen';
            }
            setTimeout(() => fitAddon.fit(), 100);
        });

        // reconnect button
        document.getElementById('reconnect').addEventListener('click', (e) => {
            e.preventDefault();
            if (socket) socket.close();
            connect();
        });

        // start everything
        term.open(document.getElementById('terminal-container'));
        fitAddon.fit();
        connect();
    </script>
</body>
</html>
"""

# ========== সার্ভার লঞ্চ ==========
async def start_server(port):
    app = web.Application()
    app.router.add_get('/', index_handler)
    app.router.add_get(WS_PATH, websocket_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Server started at http://0.0.0.0:{port} (Press Ctrl+C to stop)")
    await asyncio.Event().wait()  # চিরকাল চলবে

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    try:
        asyncio.run(start_server(port))
    except KeyboardInterrupt:
        logger.info("Shutting down...")