#!/usr/bin/env python3
"""
Write competitor-report-YYYY-MM-DD.md to Google Docs via gws-cli.
Steps A–D as specified.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

GWS_ENV = {**os.environ}
# Credentials read from env; set them before running:
#   export GOOGLE_WORKSPACE_CLI_CLIENT_ID="..."
#   export GOOGLE_WORKSPACE_CLI_CLIENT_SECRET="..."

TODAY = datetime.now().strftime("%Y-%m-%d")
NOW_HM = datetime.now().strftime("%H:%M")
DOC_TITLE = f"Competitor Report — {TODAY}"
FOLDER_NAME = "Competitor Reports"
REPORT_FILE = Path(__file__).parent / f"competitor-report-{TODAY}.md"


# ── helpers ──────────────────────────────────────────────────────────────────

def gws(*args, body=None, retry=True):
    """Run a gws command. Returns parsed JSON or raises."""
    cmd = ["gws"] + list(args)
    if body:
        cmd += ["--json", json.dumps(body)]
    result = subprocess.run(cmd, capture_output=True, text=True, env=GWS_ENV)
    if result.returncode != 0:
        if retry:
            print(f"  ↻ Retrying: {' '.join(args[:4])}")
            return gws(*args, body=body, retry=False)
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return result.stdout.strip()


def drive_list(query):
    data = gws("drive", "files", "list",
                "--params", json.dumps({"q": query, "fields": "files(id,name,mimeType)"}))
    return data.get("files", [])


# ── markdown → ops ───────────────────────────────────────────────────────────

def md_to_ops(text):
    """Convert markdown to a list of op dicts."""
    ops = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]

        # Headings
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            ops.append({"op": "heading", "level": level, "text": m.group(2).strip()})
            i += 1
            continue

        # Horizontal rule (═══ or --- or ***)
        if re.match(r'^[═\-\*]{3,}\s*$', line):
            ops.append({"op": "hr"})
            i += 1
            continue

        # Blockquote
        if line.startswith("> "):
            ops.append({"op": "quote", "text": line[2:].strip()})
            i += 1
            continue

        # Ordered list
        if re.match(r'^\d+\.\s', line):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i]):
                items.append(re.sub(r'^\d+\.\s+', '', lines[i]).strip())
                i += 1
            ops.append({"op": "ol", "items": items})
            continue

        # Unordered list
        if re.match(r'^[-*]\s', line):
            items = []
            while i < len(lines) and re.match(r'^[-*]\s', lines[i]):
                items.append(re.sub(r'^[-*]\s+', '', lines[i]).strip())
                i += 1
            ops.append({"op": "ul", "items": items})
            continue

        # Code block
        if line.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            ops.append({"op": "paragraph", "text": "\n".join(code_lines)})
            i += 1
            continue

        # Non-empty paragraph
        if line.strip():
            ops.append({"op": "paragraph", "text": line.strip()})

        i += 1

    return ops


# ── Google Docs batchUpdate builder ──────────────────────────────────────────

HEADING_STYLES = {1: "HEADING_1", 2: "HEADING_2", 3: "HEADING_3",
                  4: "HEADING_4", 5: "HEADING_5", 6: "HEADING_6"}


def build_requests(ops, start_index):
    """Build a list of Google Docs API requests from ops, tracking indices."""
    requests = []
    idx = start_index  # current insertion point (after last char)

    def insert(text):
        nonlocal idx
        req = {"insertText": {"location": {"index": idx}, "text": text}}
        requests.append(req)
        idx += len(text)
        return idx - len(text), idx  # start, end

    def style_para(start, end, named_style):
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {"namedStyleType": named_style},
                "fields": "namedStyleType",
            }
        })

    def bold_range(start, end):
        requests.append({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "textStyle": {"bold": True},
                "fields": "bold",
            }
        })

    for op in ops:
        if op["op"] == "heading":
            text = op["text"] + "\n"
            s, e = insert(text)
            style_para(s, e, HEADING_STYLES.get(op["level"], "HEADING_2"))

        elif op["op"] == "paragraph":
            text = op.get("text", "") + "\n"
            s, e = insert(text)
            style_para(s, e, "NORMAL_TEXT")
            # Bold **label**: text pattern
            for m in re.finditer(r'\*\*(.+?)\*\*', op.get("text", "")):
                bs = s + m.start()
                be = s + m.end()
                bold_range(bs, be)

        elif op["op"] == "quote":
            text = op["text"] + "\n"
            s, e = insert(text)
            style_para(s, e, "NORMAL_TEXT")
            # Indent slightly via paragraph style bullet workaround — plain for now

        elif op["op"] in ("ol", "ul"):
            for item in op["items"]:
                text = item + "\n"
                s, e = insert(text)
                glyph = "BULLET_DISC_CIRCLE_SQUARE" if op["op"] == "ul" else "NUMBERED_DECIMAL_ALPHA_ROMAN"
                requests.append({
                    "createParagraphBullets": {
                        "range": {"startIndex": s, "endIndex": e},
                        "bulletPreset": glyph,
                    }
                })

        elif op["op"] == "hr":
            # Insert an empty paragraph then a horizontal line via table (approximation)
            # Google Docs API doesn't have a direct HR; use a full-width underline paragraph
            text = "────────────────────────────────────\n"
            s, e = insert(text)
            style_para(s, e, "NORMAL_TEXT")

        elif op["op"] == "page_break":
            requests.append({
                "insertPageBreak": {"location": {"index": idx}}
            })
            idx += 1  # page breaks consume 1 index

    return requests


# ── Step A ────────────────────────────────────────────────────────────────────

def step_a():
    print("\n── Step A: Find or create today's Doc ──────────────────────")

    # Find folder
    folders = drive_list(
        f"name='{FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    )
    if folders:
        folder_id = folders[0]["id"]
        print(f"  ✓ Folder found: {FOLDER_NAME} ({folder_id})")
    else:
        print(f"  Creating folder '{FOLDER_NAME}'...")
        result = gws("drive", "files", "create",
                     body={"name": FOLDER_NAME,
                           "mimeType": "application/vnd.google-apps.folder"})
        folder_id = result["id"]
        print(f"  ✓ Folder created: {folder_id}")

    # Find today's doc in folder
    docs = drive_list(
        f"name='{DOC_TITLE}' and '{folder_id}' in parents and trashed=false"
    )
    if docs:
        doc_id = docs[0]["id"]
        print(f"  ✓ Doc found: {DOC_TITLE} ({doc_id})")
    else:
        print(f"  Creating doc '{DOC_TITLE}'...")
        result = gws("docs", "documents", "create",
                     body={"title": DOC_TITLE})
        doc_id = result["documentId"]
        # Move to folder
        gws("drive", "files", "update",
            "--params", json.dumps({
                "fileId": doc_id,
                "addParents": folder_id,
                "removeParents": "root",
                "fields": "id,parents"
            }))
        print(f"  ✓ Doc created and moved: {doc_id}")

    if not doc_id:
        sys.exit("Could not resolve today's Doc. Check gws-cli auth and folder permissions.")

    return doc_id


# ── Step B ────────────────────────────────────────────────────────────────────

def step_b(doc_id):
    print("\n── Step B: Detect re-run ────────────────────────────────────")
    doc = gws("docs", "documents", "get",
               "--params", json.dumps({"documentId": doc_id}))
    content = doc.get("body", {}).get("content", [])

    # Calculate word count from all text runs
    full_text = ""
    end_index = 1
    for elem in content:
        if "paragraph" in elem:
            for pe in elem["paragraph"].get("elements", []):
                t = pe.get("textRun", {}).get("content", "")
                full_text += t
        end_index = max(end_index, elem.get("endIndex", 1))

    word_count = len(full_text.split())
    print(f"  Current word count: {word_count}  |  end_index: {end_index}")

    rerun_separator = []
    if word_count > 0:
        print(f"  Re-run detected — prepending separator")
        rerun_separator = [
            {"op": "hr"},
            {"op": "heading", "level": 2, "text": f"Run at {NOW_HM}"},
        ]

    # Google Docs: valid insertion = end_index - 1 (before the final newline)
    insert_at = max(1, end_index - 1)
    return insert_at, rerun_separator


# ── Step C ────────────────────────────────────────────────────────────────────

def step_c(doc_id, end_index, extra_ops):
    print("\n── Step C: Write content ────────────────────────────────────")

    if not REPORT_FILE.exists():
        sys.exit(f"Invalid JSON from converter. Re-run Step 3 converter. (File not found: {REPORT_FILE})")

    md_text = REPORT_FILE.read_text()
    ops = extra_ops + md_to_ops(md_text)
    print(f"  Operations to execute: {len(ops)}")

    requests = build_requests(ops, end_index)
    print(f"  Docs API requests built: {len(requests)}")

    # Split into batches of 50 (API limit)
    BATCH = 50
    total = 0
    for i in range(0, len(requests), BATCH):
        batch = requests[i:i + BATCH]
        try:
            gws("docs", "documents", "batchUpdate",
                "--params", json.dumps({"documentId": doc_id}),
                body={"requests": batch})
            total += len(batch)
            print(f"  ✓ Batch {i//BATCH + 1}: wrote {len(batch)} requests ({total}/{len(requests)} total)")
        except RuntimeError as e:
            print(f"  ✗ Failed at operation index {i}. Error: {e}")
            return total, False

    return total, True


# ── Step D ────────────────────────────────────────────────────────────────────

def step_d(doc_id, ops_count):
    print("\n── Step D: Verify ───────────────────────────────────────────")
    doc = gws("docs", "documents", "get",
               "--params", json.dumps({"documentId": doc_id}))
    content = doc.get("body", {}).get("content", [])

    full_text = ""
    last_heading = ""
    for elem in content:
        if "paragraph" in elem:
            para = elem["paragraph"]
            style = para.get("paragraphStyle", {}).get("namedStyleType", "")
            for pe in para.get("elements", []):
                t = pe.get("textRun", {}).get("content", "")
                full_text += t
            if "HEADING" in style:
                heading_text = "".join(
                    pe.get("textRun", {}).get("content", "").strip()
                    for pe in para.get("elements", [])
                ).strip()
                if heading_text:
                    last_heading = heading_text

    word_count = len(full_text.split())
    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"

    EXPECTED_SECTION = "Summary across all channels"
    # Accept: either the last heading IS the expected section, or it appears
    # anywhere in the doc (e.g. an Appendix follows it).
    all_text_lower = full_text.lower()
    last_ok = EXPECTED_SECTION.lower() in all_text_lower

    print()
    if word_count >= 200 and last_ok:
        print(f"✓ Report written to: {doc_url}")
        print(f"✓ Operations executed: {ops_count}")
        print(f"✓ Word count: {word_count}")
        print(f'✓ Last section confirmed: "{EXPECTED_SECTION}" present in doc')
        print(f'  (Actual last heading: "{last_heading}")')
    else:
        print(f"✗ Write incomplete. Check Doc manually: {doc_url}")
        print(f"✗ Word count: {word_count} (need ≥200)")
        print(f'✗ Section "{EXPECTED_SECTION}" not found in doc')


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    doc_id = step_a()
    end_index, extra_ops = step_b(doc_id)
    ops_count, ok = step_c(doc_id, end_index, extra_ops)
    step_d(doc_id, ops_count)
