#!/usr/bin/env python3
"""Create 'NH' notebook and add 10 Nate Herk YouTube videos to it."""

import asyncio
from notebooklm import NotebookLMClient

NATE_HERK_VIDEOS = [
    "https://www.youtube.com/watch?v=9FuNtfsnRNo",   # I Built the Ultimate Team of AI Agents in n8n
    "https://www.youtube.com/watch?v=fnaTZa0-S30",   # How Nate Herk's AI Agent Is Revolutionizing Lead Response Times
    "https://www.youtube.com/watch?v=Ch-AWxvX2Jc",   # I Built a YT Strategist AI Agent That Makes Me $6k/mo
    "https://www.youtube.com/watch?v=wq001sxDTWw",   # I Built 204 AI Automations, Here's What Actually Matters
    "https://www.youtube.com/watch?v=Ey18PDiaAYI",   # Build & Sell n8n AI Agents (8+ Hour Course, No Code)
    "https://www.youtube.com/watch?v=Gc03J27xmBc",   # How I Automated Faceless Shorts with AI in n8n
    "https://www.youtube.com/watch?v=jBanaNBY-sM",   # I Built the Ultimate Army of Media Agents in n8n
    "https://www.youtube.com/watch?v=ZHH3sr234zY",   # n8n Masterclass: Build AI Agents & Automate Workflows
    "https://www.youtube.com/watch?v=cCD303XsUjI",   # From Zero to RAG Agent: Full Beginner's Course
    "https://www.youtube.com/watch?v=6w0MshwAqBQ",   # How to Create an RAG Chatbot AI Agent with n8n
]


async def main() -> None:
    async with await NotebookLMClient.from_storage() as client:
        print("Creating notebook 'NH'...")
        notebook = await client.notebooks.create(title="NH")
        print(f"  ✓ Created notebook: {notebook.title} (id={notebook.id})")

        for url in NATE_HERK_VIDEOS:
            print(f"Adding: {url}")
            source = await client.sources.add_url(notebook.id, url, wait=True)
            print(f"  ✓ Added: {source.title or url}")

    print("\nDone! Notebook 'NH' created with 10 Nate Herk videos.")


if __name__ == "__main__":
    asyncio.run(main())
