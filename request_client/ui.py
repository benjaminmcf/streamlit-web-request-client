import json

import pandas as pd
import streamlit as st

from .models import AUTH_TYPES, BODY_TYPES, METHODS, ApiResponse, HistoryEntry, RequestForm


def kv_editor(key: str) -> dict[str, str]:
    df = st.data_editor(
        pd.DataFrame({"key": pd.Series(dtype="str"), "value": pd.Series(dtype="str")}),
        key=key,
        num_rows="dynamic",
        width="stretch",
        hide_index=True,
    )
    return {
        str(k).strip(): "" if pd.isna(v) else str(v)
        for k, v in zip(df["key"], df["value"])
        if isinstance(k, str) and k.strip()
    }


def render_history(history: list[HistoryEntry]) -> bool:
    """Render the history list. Returns True if the user asked to clear it."""
    st.header("History")
    clear = st.button("Clear history", disabled=not history)
    for entry in reversed(history[-25:]):
        st.caption(f"`{entry.method}` {entry.url} → **{entry.status}**")
    return clear


def render_request_form() -> tuple[RequestForm, bool]:
    """Render the request editor. Returns the form values and whether Send was clicked."""
    form = RequestForm()

    col_method, col_url, col_send = st.columns([1, 6, 1], vertical_alignment="bottom")
    form.method = col_method.selectbox("Method", METHODS)
    form.url = col_url.text_input("URL", placeholder="http://localhost:8000/api/items")
    send = col_send.button("Send", type="primary", width="stretch")

    tab_params, tab_headers, tab_body, tab_auth, tab_opts = st.tabs(
        ["Params", "Headers", "Body", "Auth", "Options"]
    )

    with tab_params:
        form.params = kv_editor("params")

    with tab_headers:
        form.headers = kv_editor("headers")

    with tab_body:
        form.body_type = st.radio("Body type", BODY_TYPES, horizontal=True)
        if form.body_type in ("JSON", "Text"):
            form.body_text = st.text_area(
                "Body",
                height=220,
                placeholder='{"name": "example"}' if form.body_type == "JSON" else "",
            )
        elif form.body_type == "Form (urlencoded)":
            form.form_data = kv_editor("form")

    with tab_auth:
        form.auth_type = st.selectbox("Auth type", AUTH_TYPES)
        if form.auth_type == "Bearer token":
            form.token = st.text_input("Token", type="password")
        elif form.auth_type == "Basic auth":
            form.username = st.text_input("Username")
            form.password = st.text_input("Password", type="password")
        elif form.auth_type == "API key (header)":
            form.api_key_name = st.text_input("Header name", value="X-API-Key")
            form.token = st.text_input("Key", type="password")

    with tab_opts:
        form.timeout = st.number_input("Timeout (seconds)", min_value=1, max_value=300, value=30)
        form.verify = st.checkbox("Verify SSL certificates", value=True)
        form.redirects = st.checkbox("Follow redirects", value=True)

    return form, send


def _headers_table(headers: dict[str, str]) -> None:
    st.dataframe(
        pd.DataFrame(headers.items(), columns=["header", "value"]),
        width="stretch",
        hide_index=True,
    )


def render_response(result: ApiResponse | None) -> None:
    st.subheader("Response")
    if result is None:
        st.info("Send a request to see the response here.")
        return
    if result.error:
        st.error(result.error)
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Status", f"{result.status} {result.reason}")
    c2.metric("Time", f"{result.elapsed_ms:.0f} ms")
    c3.metric("Size", f"{result.size:,} B")
    if result.status >= 400:
        st.error(f"HTTP {result.status}")
    elif result.status >= 300:
        st.warning(f"HTTP {result.status}")
    else:
        st.success(f"HTTP {result.status}")
    st.caption(f"Final URL: {result.final_url}")

    tab_body, tab_raw, tab_headers, tab_req_headers = st.tabs(
        ["Body", "Raw", "Headers", "Request headers"]
    )
    with tab_body:
        content_type = result.content_type.lower()
        if "json" in content_type:
            try:
                st.json(json.loads(result.text))
            except json.JSONDecodeError:
                st.code(result.text, language="text")
        elif result.text:
            st.code(result.text, language="html" if "html" in content_type else "text")
        else:
            st.caption("(empty body)")
    with tab_raw:
        st.text_area("Raw body", result.text, height=300, label_visibility="collapsed")
    with tab_headers:
        _headers_table(result.headers)
    with tab_req_headers:
        _headers_table(result.request_headers)
