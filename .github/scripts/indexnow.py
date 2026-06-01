#!/usr/bin/env python3
"""SEO Autopilot — notify IndexNow of new/changed pages.

White-hat by design: IndexNow is the search engines' OWN instant-notification
protocol (consumed by Bing, Yandex, Naver, Seznam, Yep). It is NOT bot traffic —
it just tells crawlers "this page changed, come re-read it", which is exactly what
Google/Bing ask you to do.

Behaviour:
  * on a content push  -> submit only the pages that actually changed
  * on the weekly cron / manual run -> submit the full sitemap (light heartbeat)
Never writes to the repo, so it cannot break the live site. A non-2xx response is
logged but never fails the build (IndexNow hiccups shouldn't block anything).

The IndexNow key is intentionally NOT a secret — it is published at the key-file
URL on the site, so it is safe to keep in plain sight here.
"""
import json, os, re, subprocess, urllib.request, urllib.error

HOST     = "gotitsuperstore.co.za"
KEY      = "57181422e7dadfe49e30c63f1425e3bd"
KEYLOC   = f"https://{HOST}/{KEY}.txt"
BASE     = f"https://{HOST}/"
ENDPOINT = "https://api.indexnow.org/indexnow"   # shared across Bing/Yandex/Seznam/Naver


def sitemap_urls():
    try:
        sm = open("sitemap.xml", encoding="utf-8").read()
    except FileNotFoundError:
        return []
    return re.findall(r"<loc>([^<]+)</loc>", sm)


def file_to_url(path):
    path = path.strip()
    if not path.endswith(".html"):
        return None
    return BASE if path == "index.html" else BASE + path


def changed_html(before, after):
    if not before or set(before) <= {"0"}:   # first push / no parent
        return []
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", before, after],
            capture_output=True, text=True, check=True,
        ).stdout
    except Exception as e:                      # noqa: BLE001
        print("git diff failed, will fall back to full sitemap:", e)
        return []
    return [l for l in out.splitlines() if l.strip().endswith(".html")]


def main():
    all_urls = sitemap_urls()
    if not all_urls:
        print("No sitemap URLs found; nothing to submit.")
        return

    event = os.environ.get("GITHUB_EVENT_NAME", "")
    if event == "push":
        before = os.environ.get("BEFORE_SHA", "")
        after  = os.environ.get("AFTER_SHA", "")
        mapped = [u for u in (file_to_url(f) for f in changed_html(before, after)) if u]
        # only notify pages that are actually public (present in the sitemap)
        urls = [u for u in mapped if u in all_urls] or all_urls
    else:
        urls = all_urls

    seen = set()
    urls = [u for u in urls if not (u in seen or seen.add(u))][:10000]

    payload = {"host": HOST, "key": KEY, "keyLocation": KEYLOC, "urlList": urls}
    print(f"[IndexNow] event={event or 'manual'} -> submitting {len(urls)} URL(s):")
    for u in urls:
        print("   -", u)

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"[IndexNow] HTTP {r.status}  (200/202 = accepted)")
    except urllib.error.HTTPError as e:
        print(f"[IndexNow] HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:300]}")
    except Exception as e:                      # noqa: BLE001
        print("[IndexNow] request error (non-fatal):", e)


if __name__ == "__main__":
    main()
