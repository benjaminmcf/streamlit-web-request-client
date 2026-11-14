import streamlit as st

from request_client.client import build_spec, send_request
from request_client.models import HistoryEntry
from request_client.ui import render_history, render_request_form, render_response

st.set_page_config(page_title="Web Request Client", page_icon="🌐", layout="wide")

st.session_state.setdefault("history", [])
st.session_state.setdefault("response", None)

with st.sidebar:
    if render_history(st.session_state.history):
        st.session_state.history = []
        st.rerun()

st.title("🌐 Web Request Client")

form, send = render_request_form()

if send:
    try:
        spec = build_spec(form)
    except ValueError as exc:
        st.error(str(exc))
    else:
        with st.spinner("Sending..."):
            result = send_request(spec)
        st.session_state.response = result
        st.session_state.history.append(
            HistoryEntry(spec.method, spec.url, result.status if not result.error else "ERR")
        )
        st.rerun()

st.divider()
render_response(st.session_state.response)
