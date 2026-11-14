# streamlit-web-request-client

A simple web request client built with Streamlit, for testing APIs during development.

## Features

- Methods: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
- Query params, headers, and form fields via editable tables
- Body: JSON (validated), plain text, or URL-encoded form
- Auth: Bearer token, Basic auth, or API key header
- Options: timeout, SSL verification, follow redirects
- Response: status, time, size, pretty-printed JSON, raw body, response/request headers
- Session request history in the sidebar

## Project structure

```
app.py                  # Streamlit entry point: wires the UI to the client
request_client/
  models.py             # Dataclasses and constants (form, spec, response, history)
  client.py             # Pure logic, no Streamlit: build_spec(), send_request()
  ui.py                 # Streamlit rendering: request form, response, history
```

## Usage

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run streamlit run app.py
```

Then open http://localhost:8501.

### Changing the port

The default port is 8501. To use a different one, pass `--server.port`:

```sh
uv run streamlit run app.py --server.port 9000
```

Alternatively, set it with an environment variable:

```sh
STREAMLIT_SERVER_PORT=9000 uv run streamlit run app.py
```

Or set it permanently by creating `.streamlit/config.toml`:

```toml
[server]
port = 9000
```