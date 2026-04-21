#!/usr/bin/env python3
"""Create a NotebookLM notebook for Nate Herk's AI automation YouTube channel and add all videos."""

import asyncio
from notebooklm import NotebookLMClient

NOTEBOOK_TITLE = "Nate Herk | AI Automation"

VIDEOS = [
    # Courses & masterclasses
    ("n8n Masterclass: Build AI Agents & Automate Workflows (Beginner to Pro)", "https://www.youtube.com/watch?v=ZHH3sr234zY"),
    ("Build & Sell n8n AI Agents (8+ Hour Course, No Code)", "https://www.youtube.com/watch?v=Ey18PDiaAYI"),

    # Agent architecture & strategy
    ("Give me 15 minutes, I'll give you my entire AI agent strategy", "https://www.youtube.com/watch?v=Nj9yzBp14EM"),
    ("I built 500+ AI agents, here's everything I know", "https://www.youtube.com/watch?v=Svp7fbF0g2I"),
    ("Stop Learning n8n in 2026...Learn THIS Instead", "https://www.youtube.com/watch?v=ZeJXI2MAhj0"),

    # Multi-agent systems
    ("I Built the Ultimate Team of AI Agents in n8n With No Code (Free Template)", "https://www.youtube.com/watch?v=9FuNtfsnRNo"),
    ("Building an AI Agent Swarm in n8n Just Got So Easy", "https://www.youtube.com/watch?v=vpyllOeLhs4"),
    ("I Built an AI Agent that Builds Teams of Agents in n8n (free template)", "https://www.youtube.com/watch?v=Ik8OHT3w4pE"),
    ("I Built the Ultimate Army of Media Agents in n8n (free template)", "https://www.youtube.com/watch?v=jBanaNBY-sM"),

    # Content & social media automation
    ("I Built a 24/7 Viral Shorts Machine with No-Code (free n8n workflow)", "https://www.youtube.com/watch?v=BcfjIBd49C8"),
    ("I Built a Viral Shorts Machine for $0.75 Using AI (free n8n workflow)", "https://www.youtube.com/watch?v=jkEEVYFzT1U"),
    ("I Built an AI SYSTEM For Viral Faceless Shorts (n8n)", "https://www.youtube.com/watch?v=oMcLgseGER0"),
    ("I Built a YT Strategist AI Agent That Makes Me $6k/mo (free template n8n)", "https://www.youtube.com/watch?v=Ch-AWxvX2Jc"),

    # Scraping & data
    ("The Simplest Way to Automate Scraping Anything with No Code (Apify + n8n)", "https://www.youtube.com/watch?v=gZ_RLC25gCw"),
    ("One Tool. 4500+ Scrapers for ANYTHING. #n8n #aiagent", "https://www.youtube.com/watch?v=LveqzSr3WMQ"),

    # Business & lead automation
    ("How Nate Herk's AI Agent Is Revolutionizing Lead Response Times [With Human In The Loop]", "https://www.youtube.com/watch?v=fnaTZa0-S30"),

    # n8n techniques & advanced topics
    ("25 n8n Hacks I Wish I Knew Sooner", "https://www.youtube.com/watch?v=zMy5yoA-ub8"),
    ("Use Parallelization to Make n8n Workflows Faster & Scalable", "https://www.youtube.com/watch?v=qNW9KaLe1nY"),
    ("This AI Agent Picks Its Own Brain (10x Cheaper) #n8n #aiagent", "https://www.youtube.com/watch?v=XPB0OxPJ5g0"),

    # APIs & n8n fundamentals
    ("APIs for AI Agents Explained in Plain English #n8n #aiagent", "https://www.youtube.com/watch?v=xyJrziB4jc4"),
    ("Understanding APIs in n8n (as a beginner)", "https://www.youtube.com/watch?v=ju9xk_QX990"),
    ("n8n Tutorial #5: Access any API using the HTTP Request Node", "https://www.youtube.com/watch?v=4Ac5LlxNS8M"),
]


async def main() -> None:
    async with await NotebookLMClient.from_storage() as client:
        print(f"Creating notebook: {NOTEBOOK_TITLE!r}")
        notebook = await client.notebooks.create(NOTEBOOK_TITLE)
        print(f"  ✓ Created notebook (id={notebook.id})\n")

        for title, url in VIDEOS:
            print(f"Adding: {title}")
            source = await client.sources.add_url(notebook.id, url, wait=True)
            print(f"  ✓ {source.title or url}\n")

        print(f"Done — {len(VIDEOS)} videos added to '{NOTEBOOK_TITLE}'.")
        print(f"Notebook ID: {notebook.id}")


if __name__ == "__main__":
    asyncio.run(main())
