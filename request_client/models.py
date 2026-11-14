from dataclasses import dataclass, field
from typing import Any

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
BODY_TYPES = ["None", "JSON", "Text", "Form (urlencoded)"]
AUTH_TYPES = ["None", "Bearer token", "Basic auth", "API key (header)"]


@dataclass
class RequestForm:
    """Raw values collected from the UI."""

    method: str = "GET"
    url: str = ""
    params: dict[str, str] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
    body_type: str = "None"
    body_text: str = ""
    form_data: dict[str, str] = field(default_factory=dict)
    auth_type: str = "None"
    token: str = ""
    username: str = ""
    password: str = ""
    api_key_name: str = ""
    timeout: int = 30
    verify: bool = True
    redirects: bool = True


@dataclass
class RequestSpec:
    """A validated request, ready to be passed to `requests`."""

    method: str
    url: str
    params: dict[str, str]
    headers: dict[str, str]
    data: Any = None
    json: Any = None
    auth: tuple[str, str] | None = None
    timeout: int = 30
    verify: bool = True
    redirects: bool = True


@dataclass
class ApiResponse:
    status: int = 0
    reason: str = ""
    elapsed_ms: float = 0.0
    size: int = 0
    headers: dict[str, str] = field(default_factory=dict)
    request_headers: dict[str, str] = field(default_factory=dict)
    text: str = ""
    content_type: str = ""
    final_url: str = ""
    error: str | None = None


@dataclass
class HistoryEntry:
    method: str
    url: str
    status: int | str
