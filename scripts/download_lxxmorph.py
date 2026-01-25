#!/usr/bin/env python3
"""Download the LXX Morphology corpus directory from UPenn's gopher mirror."""
from __future__ import annotations

import argparse
import html.parser
import os
import pathlib
import re
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/"


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.links.append(value)


def fetch_bytes(url: str, user_agent: str | None = None) -> bytes:
    request = urllib.request.Request(url)
    if user_agent:
        request.add_header("User-Agent", user_agent)
    with urllib.request.urlopen(request) as response:
        return response.read()


def parse_links(content: bytes, base_url: str) -> list[str]:
    text = content.decode("utf-8", errors="replace")
    if "<a" in text.lower():
        parser = LinkParser()
        parser.feed(text)
        return [urllib.parse.urljoin(base_url, link) for link in parser.links]

    links: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("/"):
            links.append(urllib.parse.urljoin(base_url, line))
    return links


def ensure_directory(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_file(url: str, output_dir: pathlib.Path, allow_pattern: re.Pattern[str] | None, user_agent: str | None) -> None:
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename:
        return
    if allow_pattern and not allow_pattern.search(filename):
        return
    target_path = output_dir / filename
    if target_path.exists():
        return
    data = fetch_bytes(url, user_agent=user_agent)
    target_path.write_bytes(data)


def download_recursive(
    base_url: str,
    output_dir: pathlib.Path,
    visited: set[str],
    allow_pattern: re.Pattern[str] | None,
    user_agent: str | None,
) -> None:
    if base_url in visited:
        return
    visited.add(base_url)

    content = fetch_bytes(base_url, user_agent=user_agent)
    links = parse_links(content, base_url)
    for link in links:
        if link.endswith("/"):
            subdir_name = os.path.basename(os.path.normpath(urllib.parse.urlparse(link).path))
            subdir_path = output_dir / subdir_name
            ensure_directory(subdir_path)
            download_recursive(link, subdir_path, visited, allow_pattern, user_agent)
        else:
            save_file(link, output_dir, allow_pattern, user_agent)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download files from the LXX Morphology directory.")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Base URL for the LXX Morphology directory listing.",
    )
    parser.add_argument(
        "--include",
        default="\\.mlxx$",
        help="Regex pattern of filenames to download (default: only .mlxx files).",
    )
    parser.add_argument(
        "--output-dir",
        default="lxxmorph",
        help="Directory to store downloaded files.",
    )
    parser.add_argument(
        "--user-agent",
        default="Mozilla/5.0 (compatible; LXXMorphDownloader/1.0)",
        help="User-Agent header to send with requests.",
    )
    args = parser.parse_args()

    output_dir = pathlib.Path(args.output_dir)
    ensure_directory(output_dir)
    allow_pattern = re.compile(args.include) if args.include else None
    download_recursive(args.base_url, output_dir, set(), allow_pattern, args.user_agent)


if __name__ == "__main__":
    main()
