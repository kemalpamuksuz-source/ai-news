#!/usr/bin/env bash
# Daily competitor intelligence runner — called by cron at 21:00
set -euo pipefail

REPO="/home/user/ai-news"
LOG="$REPO/competitor-intelligence.log"
TODAY=$(date +%Y-%m-%d)

exec >> "$LOG" 2>&1
echo "========================================"
echo "Run started: $(date)"

# Require credentials in environment
if [[ -z "${GOOGLE_WORKSPACE_CLI_CLIENT_ID:-}" || -z "${GOOGLE_WORKSPACE_CLI_CLIENT_SECRET:-}" ]]; then
  echo "ERROR: GOOGLE_WORKSPACE_CLI_CLIENT_ID and GOOGLE_WORKSPACE_CLI_CLIENT_SECRET must be set."
  exit 1
fi

export GOOGLE_WORKSPACE_CLI_CLIENT_ID
export GOOGLE_WORKSPACE_CLI_CLIENT_SECRET

cd "$REPO"

# Step 1: Try yt-dlp for each channel (best-effort; silently skip on 403)
CHANNELS=(
  "https://www.youtube.com/@mreflow"
  "https://www.youtube.com/@AIJasonZ"
  "https://www.youtube.com/@DavidOndrej"
  "https://www.youtube.com/@GregIsenberg"
  "https://www.youtube.com/@yoheinakajima"
)

CUTOFF=$(date -d '24 hours ago' +%s 2>/dev/null || date -v-1d +%s)
YT_DATA=""

for CH in "${CHANNELS[@]}"; do
  HANDLE=$(basename "$CH")
  echo "Fetching $HANDLE ..."
  RAW=$(yt-dlp \
    --flat-playlist \
    --playlist-end 5 \
    --print "%(id)s|%(title)s|%(timestamp)s|%(view_count)s|%(duration)s|%(uploader)s" \
    "$CH" 2>/dev/null || true)
  if [[ -n "$RAW" ]]; then
    while IFS='|' read -r id title ts views dur uploader; do
      if [[ -n "$ts" && "$ts" -ge "$CUTOFF" ]] 2>/dev/null; then
        YT_DATA+="NEW|$uploader|$title|$id|$views|$dur"$'\n'
      fi
    done <<< "$RAW"
  fi
done

echo "yt-dlp new-video lines found: $(echo "$YT_DATA" | grep -c NEW || true)"

# Step 2: Write the markdown report using Claude (via claude CLI) or fall back to a stub
REPORT_FILE="$REPO/competitor-report-$TODAY.md"

if command -v claude &>/dev/null; then
  # Ask Claude to write the report using gathered data
  YT_CONTEXT=""
  if [[ -n "$YT_DATA" ]]; then
    YT_CONTEXT="New videos found in last 24h:\n$YT_DATA"
  else
    YT_CONTEXT="yt-dlp returned no data (network may be restricted). Use web search for each channel."
  fi

  claude --print --no-conversation \
    "You are running the Competitor Intelligence pipeline. Today is $TODAY.
$YT_CONTEXT

Write a competitor report markdown file to: $REPORT_FILE

Channels: Matt Wolfe (@mreflow), AI Jason (@AIJasonZ), David Ondrej (@DavidOndrej), Greg Isenberg (@GregIsenberg), Yohei Nakajima (@yoheinakajima).

Use the data above. If no data, use web search for recent videos in the last 24h. Follow the report format from the competitor-intelligence skill. Include the 'Summary across all channels' section. Write the file directly." \
    2>&1 || true
else
  echo "WARNING: claude CLI not found; skipping AI report generation."
fi

# Step 3: Publish to Google Doc (only if report exists)
if [[ -f "$REPORT_FILE" ]]; then
  echo "Publishing to Google Doc..."
  python "$REPO/write_to_gdoc.py"
else
  echo "ERROR: Report file not found at $REPORT_FILE — skipping publish."
  exit 1
fi

echo "Run complete: $(date)"
echo "========================================"
