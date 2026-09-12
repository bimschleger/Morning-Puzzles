"""
Morning Puzzles - Web Service API
Serves daily puzzles in JSON format, pure ESC/POS text, and hybrid 1-bit raster formats
optimized for commercial 80mm thermal receipt printers.
Supports FastAPI (when installed) with fallback to Python's built-in http.server.
"""

import sys
import os
import json
import datetime
from urllib.parse import urlparse, parse_qs

# Add parent directory to path to allow importing app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.generators.sudoku_gen import SudokuGenerator
from app.generators.wordsearch_gen import WordSearchGenerator
from app.generators.nonogram_gen import NonogramGenerator
from app.generators.queens_gen import QueensGenerator
from app.generators.jumble_gen import JumbleGenerator
from app.generators.binary_gen import BinaryGenerator
from app.generators.mines_gen import MinesGenerator
from app.renderer.text_formatter import (
    build_daily_receipt_bytes,
    build_hybrid_daily_receipt_bytes,
    EscPosTextReceipt,
)

# Initialize generators
sudoku_gen = SudokuGenerator()
wordsearch_gen = WordSearchGenerator()
nonogram_gen = NonogramGenerator()
queens_gen = QueensGenerator()
jumble_gen = JumbleGenerator()
binary_gen = BinaryGenerator()
mines_gen = MinesGenerator()


def generate_daily_bundle(difficulty: str = "medium") -> dict:
    today_str = datetime.date.today().strftime("%A, %B %d, %Y")
    return {
        "title": "DAILY MORNING PUZZLES",
        "date": today_str,
        "difficulty": difficulty,
        "sudoku": sudoku_gen.generate(difficulty=difficulty),
        "wordsearch": wordsearch_gen.generate(difficulty=difficulty),
        "nonogram": nonogram_gen.generate(difficulty="easy" if difficulty == "easy" else "medium"),
        "queens": queens_gen.generate(difficulty=difficulty),
        "jumble": jumble_gen.generate(difficulty=difficulty),
        "binary": binary_gen.generate(difficulty=difficulty),
        "mines": mines_gen.generate(difficulty=difficulty),
    }


# ==============================================================================
# 1. FastAPI Application (Used when running via uvicorn)
# ==============================================================================
try:
    from fastapi import FastAPI, Query, Response
    from fastapi.responses import JSONResponse, HTMLResponse

    app = FastAPI(
        title="Morning Puzzles API",
        description="API generating daily puzzles for 80mm commercial thermal printers (576 dots width)",
        version="1.1.0"
    )

    SIMULATOR_HTML_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "simulator",
        "receipt_simulator.html"
    )

    @app.get("/", response_class=HTMLResponse)
    @app.get("/simulator", response_class=HTMLResponse)
    def get_simulator():
        if os.path.exists(SIMULATOR_HTML_PATH):
            with open(SIMULATOR_HTML_PATH, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        return HTMLResponse(content="<h1>Simulator file not found</h1>", status_code=404)

    @app.get("/health")
    def health():
        return {"status": "ok", "time": datetime.datetime.now().isoformat()}

    @app.get("/api/v1/daily-print")
    def get_daily_print(
        format: str = Query("escpos", regex="^(escpos|json)$"),
        difficulty: str = Query("medium", regex="^(easy|medium|hard)$"),
        style: str = Query("hybrid", regex="^(hybrid|text)$")
    ):
        bundle = generate_daily_bundle(difficulty=difficulty)
        if format == "json":
            return JSONResponse(content=bundle)

        # Build binary ESC/POS stream for thermal printer
        if style == "text":
            escpos_bytes = build_daily_receipt_bytes(bundle)
        else:
            escpos_bytes = build_hybrid_daily_receipt_bytes(bundle)

        return Response(
            content=escpos_bytes,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": "inline; filename=morning-puzzles.bin",
                "Content-Length": str(len(escpos_bytes))
            }
        )

    @app.get("/api/v1/test-print")
    def get_test_print():
        r = EscPosTextReceipt()
        r.header("TEST RECEIPT", datetime.date.today().strftime("%Y-%m-%d"))
        r.println("ESP32 <-> Thermal Printer link is operational!")
        r.println("576-dot 80mm thermal receipt verified.")
        r.feed(4)
        r.cut()
        data = r.get_bytes()
        return Response(content=data, media_type="application/octet-stream")

    @app.get("/api/v1/puzzles/sudoku")
    def get_sudoku(difficulty: str = "medium"):
        return sudoku_gen.generate(difficulty=difficulty)

    @app.get("/api/v1/puzzles/wordsearch")
    def get_wordsearch(difficulty: str = "medium"):
        return wordsearch_gen.generate(difficulty=difficulty)

    @app.get("/api/v1/puzzles/nonogram")
    def get_nonogram(difficulty: str = "medium"):
        return nonogram_gen.generate(difficulty=difficulty)

    @app.get("/api/v1/puzzles/queens")
    def get_queens(difficulty: str = "medium"):
        return queens_gen.generate(difficulty=difficulty)

    @app.get("/api/v1/puzzles/jumble")
    def get_jumble(difficulty: str = "medium"):
        return jumble_gen.generate(difficulty=difficulty)

    @app.get("/api/v1/puzzles/binary")
    def get_binary(difficulty: str = "medium"):
        return binary_gen.generate(difficulty=difficulty)

    @app.get("/api/v1/puzzles/mines")
    def get_mines(difficulty: str = "medium"):
        return mines_gen.generate(difficulty=difficulty)

except ImportError:
    app = None


# ==============================================================================
# 2. Built-in HTTP Server Fallback (Runs on any machine with Python 3)
# ==============================================================================
def run_standalone_server(port: int = 8000, host: str = "0.0.0.0"):
    from http.server import HTTPServer, BaseHTTPRequestHandler

    class PuzzleHttpHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            query_params = parse_qs(parsed.query)
            path = parsed.path

            if path in ("/simulator", "/"):
                sim_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                    "simulator",
                    "receipt_simulator.html"
                )
                if os.path.exists(sim_path):
                    with open(sim_path, "rb") as f:
                        data = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Simulator not found")
            elif path == "/health":
                self._send_json(200, {"status": "ok", "time": datetime.datetime.now().isoformat()})
            elif path == "/api/v1/daily-print":
                fmt = query_params.get("format", ["escpos"])[0]
                diff = query_params.get("difficulty", ["medium"])[0]
                style = query_params.get("style", ["hybrid"])[0]
                bundle = generate_daily_bundle(diff)

                if fmt == "json":
                    self._send_json(200, bundle)
                else:
                    if style == "text":
                        escpos_data = build_daily_receipt_bytes(bundle)
                    else:
                        escpos_data = build_hybrid_daily_receipt_bytes(bundle)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/octet-stream")
                    self.send_header("Content-Length", str(len(escpos_data)))
                    self.end_headers()
                    self.wfile.write(escpos_data)
            elif path == "/api/v1/test-print":
                r = EscPosTextReceipt()
                r.header("TEST RECEIPT", datetime.date.today().strftime("%Y-%m-%d"))
                r.println("ESP32 <-> Thermal Printer link is operational!")
                r.println("576-dot 80mm thermal receipt verified.")
                r.feed(4)
                r.cut()
                data = r.get_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            elif path == "/api/v1/puzzles/sudoku":
                diff = query_params.get("difficulty", ["medium"])[0]
                self._send_json(200, sudoku_gen.generate(difficulty=diff))
            elif path == "/api/v1/puzzles/wordsearch":
                diff = query_params.get("difficulty", ["medium"])[0]
                self._send_json(200, wordsearch_gen.generate(difficulty=diff))
            elif path == "/api/v1/puzzles/nonogram":
                diff = query_params.get("difficulty", ["medium"])[0]
                self._send_json(200, nonogram_gen.generate(difficulty=diff))
            elif path == "/api/v1/puzzles/queens":
                diff = query_params.get("difficulty", ["medium"])[0]
                self._send_json(200, queens_gen.generate(difficulty=diff))
            elif path == "/api/v1/puzzles/jumble":
                diff = query_params.get("difficulty", ["medium"])[0]
                self._send_json(200, jumble_gen.generate(difficulty=diff))
            elif path == "/api/v1/puzzles/binary":
                diff = query_params.get("difficulty", ["medium"])[0]
                self._send_json(200, binary_gen.generate(difficulty=diff))
            elif path == "/api/v1/puzzles/mines":
                diff = query_params.get("difficulty", ["medium"])[0]
                self._send_json(200, mines_gen.generate(difficulty=diff))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404 Not Found")

        def _send_json(self, status: int, data: dict):
            payload = json.dumps(data, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

    server = HTTPServer((host, port), PuzzleHttpHandler)
    print(f"\n[SERVER] Morning Puzzles Server running at http://{host}:{port}/")
    print(f"[SERVER] Daily Print Endpoint: http://{host}:{port}/api/v1/daily-print")
    print(f"[SERVER] Test Print Endpoint:  http://{host}:{port}/api/v1/test-print")
    print("[SERVER] Press Ctrl+C to terminate.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER] Server shutting down.")
        server.server_close()


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_standalone_server(port=port)
