# Web Related Notes

## Current examples
- `open_browser.py`: CLI helpers to open URLs and generate link snippets.
- `reqeust_tute.py`: Requests basics with timeouts, headers, JSON/form examples, session cookies.
- `wallpaper/`: Wallpaper downloader with endpoint from `config.toml`.
- `websockets_examples/quick_start/`: Minimal ws echo server/client.
- `web_scraping/selenium_example.py`: Selenium demo (headless-friendly with options).
- `servers/pic_server/`: Simple image server utilities.
- `sockets/socket_prog_tute/`: Low-level socket echo samples.

## Gaps and suggested additions
1) Add `httpx` async examples mirroring the requests tutorial (timeouts, connection pooling, concurrency).
2) Add retry/backoff utilities (shared helper used by requests/httpx) with logging and circuit-breaker style guard.
3) WebSocket robustness: reconnect loop, heartbeat/ping, graceful shutdown, plus pytestable echo test.
4) Observability: add a small logging setup (structured JSON option) for server/client scripts.
5) Security ergonomics: examples for auth headers, signed URLs, and secrets management via env vars instead of literals.
6) Testing: lightweight integration tests that spin up local echo servers (http + ws) and verify clients.

## Quick tips
- Always set `timeout` on outbound calls; prefer sessions or clients for connection reuse.
- Avoid printing full response bodies; log status, headers, and sample slices instead.
- Validate config files and create output directories before writing.
- Prefer `pathlib.Path` and `argparse` for scripts so they remain CLI-friendly.
