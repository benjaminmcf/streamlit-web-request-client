import json

import requests

from .models import ApiResponse, RequestForm, RequestSpec


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        raise ValueError("Enter a URL.")
    return url if "://" in url else "http://" + url


def build_spec(form: RequestForm) -> RequestSpec:
    """Validate the form and convert it into a RequestSpec. Raises ValueError."""
    headers = dict(form.headers)
    auth = None
    if form.auth_type == "Bearer token" and form.token:
        headers["Authorization"] = f"Bearer {form.token}"
    elif form.auth_type == "Basic auth":
        auth = (form.username, form.password)
    elif form.auth_type == "API key (header)" and form.token and form.api_key_name:
        headers[form.api_key_name] = form.token

    json_body = None
    data = None
    if form.body_type == "JSON" and form.body_text.strip():
        try:
            json_body = json.loads(form.body_text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON body: {exc}") from exc
    elif form.body_type == "Text" and form.body_text:
        data = form.body_text.encode()
    elif form.body_type == "Form (urlencoded)" and form.form_data:
        data = form.form_data

    return RequestSpec(
        method=form.method,
        url=normalize_url(form.url),
        params=form.params,
        headers=headers,
        data=data,
        json=json_body,
        auth=auth,
        timeout=form.timeout,
        verify=form.verify,
        redirects=form.redirects,
    )


def send_request(spec: RequestSpec) -> ApiResponse:
    try:
        resp = requests.request(
            spec.method,
            spec.url,
            params=spec.params,
            headers=spec.headers,
            data=spec.data,
            json=spec.json,
            auth=spec.auth,
            timeout=spec.timeout,
            verify=spec.verify,
            allow_redirects=spec.redirects,
        )
    except requests.RequestException as exc:
        return ApiResponse(error=f"{type(exc).__name__}: {exc}")
    return ApiResponse(
        status=resp.status_code,
        reason=resp.reason,
        elapsed_ms=resp.elapsed.total_seconds() * 1000,
        size=len(resp.content),
        headers=dict(resp.headers),
        request_headers=dict(resp.request.headers),
        text=resp.text,
        content_type=resp.headers.get("Content-Type", ""),
        final_url=resp.url,
    )
