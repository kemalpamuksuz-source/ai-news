#!/usr/bin/env python3
"""Create the Nate Herk | AI Automation NotebookLM notebook and add all videos.

Equivalent to running:
  python add_to_notebook.py --new "Nate Herk | AI Automation" <url1> <url2> ...
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from add_to_notebook import create_and_add

NOTEBOOK_TITLE = "Nate Herk | AI Automation"

VIDEOS = [
    # Courses & masterclasses
    "https://www.youtube.com/watch?v=ZHH3sr234zY",  # n8n Masterclass: Build AI Agents & Automate Workflows (Beginner to Pro)
    "https://www.youtube.com/watch?v=Ey18PDiaAYI",  # Build & Sell n8n AI Agents (8+ Hour Course, No Code)

    # Agent architecture & strategy
    "https://www.youtube.com/watch?v=Nj9yzBp14EM",  # Give me 15 minutes, I'll give you my entire AI agent strategy
    "https://www.youtube.com/watch?v=Svp7fbF0g2I",  # I built 500+ AI agents, here's everything I know
    "https://www.youtube.com/watch?v=ZeJXI2MAhj0",  # Stop Learning n8n in 2026...Learn THIS Instead

    # Multi-agent systems
    "https://www.youtube.com/watch?v=9FuNtfsnRNo",  # I Built the Ultimate Team of AI Agents in n8n With No Code
    "https://www.youtube.com/watch?v=vpyllOeLhs4",  # Building an AI Agent Swarm in n8n Just Got So Easy
    "https://www.youtube.com/watch?v=Ik8OHT3w4pE",  # I Built an AI Agent that Builds Teams of Agents in n8n
    "https://www.youtube.com/watch?v=jBanaNBY-sM",  # I Built the Ultimate Army of Media Agents in n8n

    # Content & social media automation
    "https://www.youtube.com/watch?v=BcfjIBd49C8",  # I Built a 24/7 Viral Shorts Machine with No-Code
    "https://www.youtube.com/watch?v=jkEEVYFzT1U",  # I Built a Viral Shorts Machine for $0.75 Using AI
    "https://www.youtube.com/watch?v=oMcLgseGER0",  # I Built an AI SYSTEM For Viral Faceless Shorts (n8n)
    "https://www.youtube.com/watch?v=Ch-AWxvX2Jc",  # I Built a YT Strategist AI Agent That Makes Me $6k/mo

    # Scraping & data
    "https://www.youtube.com/watch?v=gZ_RLC25gCw",  # The Simplest Way to Automate Scraping Anything with No Code
    "https://www.youtube.com/watch?v=LveqzSr3WMQ",  # One Tool. 4500+ Scrapers for ANYTHING.

    # Business & lead automation
    "https://www.youtube.com/watch?v=fnaTZa0-S30",  # How Nate Herk's AI Agent Is Revolutionizing Lead Response Times

    # n8n techniques & advanced topics
    "https://www.youtube.com/watch?v=zMy5yoA-ub8",  # 25 n8n Hacks I Wish I Knew Sooner
    "https://www.youtube.com/watch?v=qNW9KaLe1nY",  # Use Parallelization to Make n8n Workflows Faster & Scalable
    "https://www.youtube.com/watch?v=XPB0OxPJ5g0",  # This AI Agent Picks Its Own Brain (10x Cheaper)

    # APIs & n8n fundamentals
    "https://www.youtube.com/watch?v=xyJrziB4jc4",  # APIs for AI Agents Explained in Plain English
    "https://www.youtube.com/watch?v=ju9xk_QX990",  # Understanding APIs in n8n (as a beginner)
    "https://www.youtube.com/watch?v=4Ac5LlxNS8M",  # n8n Tutorial #5: Access any API using the HTTP Request Node
]

if __name__ == "__main__":
    asyncio.run(create_and_add(NOTEBOOK_TITLE, VIDEOS))
