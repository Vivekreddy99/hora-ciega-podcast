#!/usr/bin/env python3
"""Generate a valid podcast RSS (feed.xml) from podcast.json. Spotify/Apple-compatible."""
import json, os, html, datetime, email.utils

HERE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(HERE, "podcast.json")))
B = cfg["base_url"].rstrip("/")

def esc(s): return html.escape(s or "", quote=True)
def rfc(d):  # 'YYYY-MM-DD' -> RFC-2822
    dt = datetime.datetime.strptime(d, "%Y-%m-%d")
    return email.utils.format_datetime(dt.replace(tzinfo=datetime.timezone.utc))
def hhmmss(sec):
    sec = int(round(float(sec))); h, r = divmod(sec, 3600); m, s = divmod(r, 60)
    return f"{h:d}:{m:02d}:{s:02d}"

items = []
for e in cfg["episodes"]:
    url = f"{B}/{e['file']}"
    items.append(f"""    <item>
      <title>{esc(e['title'])}</title>
      <description>{esc(e['description'])}</description>
      <itunes:summary>{esc(e['description'])}</itunes:summary>
      <enclosure url="{esc(url)}" length="{e['bytes']}" type="audio/mpeg"/>
      <guid isPermaLink="false">horaciega-{e['num']}</guid>
      <pubDate>{rfc(e['pubDate'])}</pubDate>
      <itunes:duration>{hhmmss(e['duration'])}</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
      <itunes:episode>{int(e['num'])}</itunes:episode>
    </item>""")

feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{esc(cfg['title'])}</title>
    <link>{esc(cfg['link'])}</link>
    <language>{esc(cfg['language'])}</language>
    <description>{esc(cfg['description'])}</description>
    <itunes:summary>{esc(cfg['description'])}</itunes:summary>
    <itunes:author>{esc(cfg['author'])}</itunes:author>
    <itunes:type>episodic</itunes:type>
    <itunes:explicit>false</itunes:explicit>
    <itunes:owner>
      <itunes:name>{esc(cfg['author'])}</itunes:name>
      <itunes:email>{esc(cfg['owner_email'])}</itunes:email>
    </itunes:owner>
    <itunes:image href="{esc(B + '/' + cfg['cover'])}"/>
    <itunes:category text="{esc(cfg['category'])}"/>
    <image><url>{esc(B + '/' + cfg['cover'])}</url><title>{esc(cfg['title'])}</title><link>{esc(cfg['link'])}</link></image>
{os.linesep.join(items)}
  </channel>
</rss>
"""
open(os.path.join(HERE, "feed.xml"), "w").write(feed)
print(f"feed.xml written — {len(cfg['episodes'])} episode(s)")
