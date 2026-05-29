"""Thin urllib wrapper around the SonarQube Web API.

Two endpoints used:
  - GET /api/issues/search    (paginated; returns issues + components)
  - POST /api/issues/set_tags (write-back; only invoked from tagger.py)

For offline tests, an HTTP URL of the form `file://path/to/payload.json` is
treated as a single canned response (no pagination). Use this with the
sample fixture for `tlctc-sonar classify` smoke runs.
"""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Iterator


class SonarApiError(RuntimeError):
    """Raised on Sonar API auth / HTTP errors."""


class SonarTransportError(RuntimeError):
    """Raised on network / 5xx failures."""


@dataclass(frozen=True)
class SonarClient:
    base_url: str
    token: str
    timeout: float = 30.0

    def _auth_header(self) -> str:
        # SonarQube tokens use HTTP Basic with token as username, empty password.
        raw = f"{self.token}:".encode("utf-8")
        return "Basic " + base64.b64encode(raw).decode("ascii")

    def is_offline_fixture(self) -> bool:
        return self.base_url.startswith("file://")

    def search_issues(
        self,
        project_keys: list[str] | None = None,
        component_keys: list[str] | None = None,
        branch: str | None = None,
        pull_request: str | None = None,
        created_after: str | None = None,
        severities: list[str] | None = None,
        types: list[str] | None = None,
        page_size: int = 100,
        max_pages: int = 50,
    ) -> Iterator[dict]:
        """Yield issue dicts. Handles pagination. Honors file:// for offline tests."""
        if self.is_offline_fixture():
            yield from self._read_offline_fixture()
            return

        params: dict[str, str] = {"ps": str(page_size)}
        if project_keys:
            params["projects"] = ",".join(project_keys)
        if component_keys:
            params["componentKeys"] = ",".join(component_keys)
        if branch:
            params["branch"] = branch
        if pull_request:
            params["pullRequest"] = pull_request
        if created_after:
            params["createdAfter"] = created_after
        if severities:
            params["severities"] = ",".join(severities)
        if types:
            params["types"] = ",".join(types)

        for page in range(1, max_pages + 1):
            params["p"] = str(page)
            payload = self._get("/api/issues/search", params)
            issues = payload.get("issues", []) or []
            for issue in issues:
                yield issue
            paging = payload.get("paging", {})
            total = int(paging.get("total", 0) or 0)
            if page * page_size >= total:
                return
            if not issues:
                return

    def set_tags(self, issue_key: str, tags: list[str]) -> None:
        """Replace the tag set on a single Sonar issue."""
        if self.is_offline_fixture():
            raise SonarApiError("cannot apply tags against a file:// fixture")
        body = urllib.parse.urlencode({"issue": issue_key, "tags": ",".join(tags)}).encode("ascii")
        req = urllib.request.Request(
            url=self._url("/api/issues/set_tags"),
            data=body,
            method="POST",
            headers={
                "Authorization": self._auth_header(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                resp.read()  # discard
        except urllib.error.HTTPError as exc:
            raise SonarApiError(f"set_tags {issue_key}: HTTP {exc.code} {exc.reason}") from exc
        except urllib.error.URLError as exc:
            raise SonarTransportError(f"set_tags {issue_key}: {exc.reason}") from exc

    def _get(self, endpoint: str, params: dict[str, str]) -> dict:
        url = self._url(endpoint) + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(
            url=url,
            method="GET",
            headers={
                "Authorization": self._auth_header(),
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise SonarApiError(f"{endpoint}: HTTP {exc.code} {exc.reason}") from exc
        except urllib.error.URLError as exc:
            raise SonarTransportError(f"{endpoint}: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise SonarApiError(f"{endpoint}: invalid JSON response: {exc}") from exc

    def _url(self, endpoint: str) -> str:
        return self.base_url.rstrip("/") + endpoint

    def _read_offline_fixture(self) -> Iterator[dict]:
        from pathlib import Path

        path = self.base_url[len("file://"):]
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        for issue in data.get("issues", []) or []:
            yield issue
