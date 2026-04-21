#!/usr/bin/env python3
"""Manage NotebookLM notebooks.

Usage:
  # Create a new notebook and add URLs to it
  python add_to_notebook.py --new "Notebook Title" <url1> [url2 ...]

  # Add URLs to an existing notebook
  python add_to_notebook.py <notebook_id> <url1> [url2 ...]

  # List all existing notebooks
  python add_to_notebook.py --list
"""

import asyncio
import sys
from notebooklm import NotebookLMClient


async def list_notebooks() -> None:
    async with await NotebookLMClient.from_storage() as client:
        notebooks = await client.notebooks.list()
        if not notebooks:
            print("No notebooks found.")
            return
        print(f"{'Title':<40} {'ID'}")
        print("-" * 80)
        for nb in notebooks:
            print(f"{nb.title:<40} {nb.id}")


async def create_and_add(title: str, urls: list[str]) -> None:
    async with await NotebookLMClient.from_storage() as client:
        print(f"Creating notebook: {title!r}")
        notebook = await client.notebooks.create(title)
        print(f"  ✓ Created (id={notebook.id})\n")
        await _add_urls(client, notebook.id, urls)


async def add_urls(notebook_id: str, urls: list[str]) -> None:
    async with await NotebookLMClient.from_storage() as client:
        await _add_urls(client, notebook_id, urls)


async def _add_urls(client: NotebookLMClient, notebook_id: str, urls: list[str]) -> None:
    for url in urls:
        print(f"Adding: {url}")
        source = await client.sources.add_url(notebook_id, url, wait=True)
        print(f"  ✓ Added: {source.title or url}")


def usage() -> None:
    print(__doc__)
    sys.exit(1)


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        usage()

    if args[0] == "--list":
        asyncio.run(list_notebooks())

    elif args[0] == "--new":
        if len(args) < 3:
            print("Error: --new requires a title and at least one URL.")
            usage()
        title = args[1]
        urls = args[2:]
        asyncio.run(create_and_add(title, urls))

    else:
        if len(args) < 2:
            print("Error: provide a notebook ID and at least one URL.")
            usage()
        notebook_id = args[0]
        urls = args[1:]
        asyncio.run(add_urls(notebook_id, urls))
