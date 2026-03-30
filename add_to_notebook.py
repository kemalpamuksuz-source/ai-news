#!/usr/bin/env python3
"""Add URLs to a NotebookLM notebook. Usage: python add_to_notebook.py <notebook_id> <url1> [url2 ...]"""

import asyncio
import sys
from notebooklm import NotebookLMClient


async def add_urls(notebook_id: str, urls: list[str]) -> None:
    async with await NotebookLMClient.from_storage() as client:
        for url in urls:
            print(f"Adding: {url}")
            source = await client.sources.add_url(notebook_id, url, wait=True)
            print(f"  ✓ Added: {source.title or url}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python add_to_notebook.py <notebook_id> <url1> [url2 ...]")
        sys.exit(1)

    notebook_id = sys.argv[1]
    urls = sys.argv[2:]
    asyncio.run(add_urls(notebook_id, urls))
