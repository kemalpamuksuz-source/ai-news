═══════════════════════════════════════
# Daily Competitor Report

**Date:** 2026-05-29  
**Channels tracked:** 5  
**New videos:** 0 confirmed within 24h

> ⚠️ **Data-collection note:** This environment blocks outbound connections to
> `youtube.com` at the network level (`x-deny-reason: host_not_allowed`),
> identical to the restriction that blocks `notebooklm.google.com`. `yt-dlp`
> exits with HTTP 403 on every channel. YouTube RSS feeds and all major
> third-party analytics/transcript services (Viewstats, SocialBlade,
> YouTubeToTranscript, Recall, Metacast, Podchaser) also returned 403.
> View counts, durations, and transcripts could not be retrieved programmatically.
> Metadata below is sourced from web-search index snippets only; no data has
> been invented. To run this workflow fully, execute it from a machine without
> YouTube egress restrictions, or use a proxy/VPN tunnel.

---

## Matt Wolfe — No new video

No video confirmed published within the last 24 hours on @mreflow.

**Last known upload (search index):** "AI News: These Google Updates Are Dividing
People" — approx. 2026-05-19.  
**Link:** https://www.youtube.com/watch?v=OYyS0Gu5xj8 (most recent confirmed via
search; may not be the actual latest upload — channel is not directly accessible)

---

## AI Jason — No new video

No video confirmed published within the last 24 hours on @AIJasonZ.

**Last known activity:** Channel is active; no specific video title or date
retrieved from search index for the 2026-05-28/29 window.

---

## David Ondrej — No new video

No video confirmed published within the last 24 hours on @DavidOndrej.

**Closest recent upload:** "The Philosophy of David Ondrej" — approx. 2026-05-27
(search snippet showed "2 days ago" as of 2026-05-29, placing it outside the
24h window).  
**Link:** https://www.youtube.com/watch?v=_9-8s6zMwhc

---

## Greg Isenberg — No new video

No video confirmed published within the last 24 hours on @GregIsenberg.

**Last known activity:** The Startup Ideas Podcast publishes twice weekly.
No specific episode title or date retrieved for the 2026-05-28/29 window.

---

## Yohei Nakajima — No new video

No video confirmed published within the last 24 hours on @yoheinakajima.

**Adjacent activity (not a video):** Published arXiv paper
"The Log is the Agent: Event-Sourced Reactive Graphs for Auditable, Forkable
Agentic Systems" on or around 2026-05-22. No YouTube upload found for this week.

---

## Summary across all channels

**Common theme today:** No new videos confirmed; cannot assess themes.

**Outliers:** Yohei Nakajima is the only creator with verifiable new public output
this week — an arXiv paper on event-sourced agentic systems, not a video.

**Highest signal video for the user today:** None confirmed in the 24h window.
If the window is relaxed to ~10 days, David Ondrej's "The Philosophy of David
Ondrej" (2026-05-27) is worth investigating for overlap with your AI-agency
positioning content. Yohei's arXiv paper directly overlaps with your AI agents
and Claude Routines topics — worth reading regardless of video form.

═══════════════════════════════════════

## Appendix: How to run this report correctly

```bash
# From a machine with unrestricted YouTube access:
pip install yt-dlp

CHANNELS=(
  "https://www.youtube.com/@mreflow"
  "https://www.youtube.com/@AIJasonZ"
  "https://www.youtube.com/@DavidOndrej"
  "https://www.youtube.com/@GregIsenberg"
  "https://www.youtube.com/@yoheinakajima"
)

CUTOFF=$(date -d '24 hours ago' +%s)

for CH in "${CHANNELS[@]}"; do
  yt-dlp \
    --flat-playlist \
    --playlist-end 5 \
    --print "%(id)s|%(title)s|%(timestamp)s|%(view_count)s|%(duration)s|%(uploader)s" \
    "$CH"
done
```

Then for each video ID within the cutoff window, pull transcript:

```bash
yt-dlp \
  --write-auto-sub \
  --sub-lang en \
  --skip-download \
  --output "%(id)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```
