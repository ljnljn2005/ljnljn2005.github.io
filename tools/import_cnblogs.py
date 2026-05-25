from __future__ import annotations

import argparse
import datetime as dt
import html
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xmlrpc.client
from pathlib import Path

try:
    from markdownify import markdownify as html_to_markdown
except Exception:  # pragma: no cover - optional local dependency
    html_to_markdown = None


ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "source" / "_posts"
ASSETS_DIR = ROOT / "source" / "assets" / "cnblogs"

SKIP_TITLES = {
    "友链",
    "新blog",
    "3月社团练习赛WP",
    "2026FIC决赛复现wp",
}

IMAGE_MARKDOWN_RE = re.compile(r"!\[[^\]]*\]\(([^)\n]+)\)")
IMAGE_HTML_RE = re.compile(r"""(<img\b[^>]*\bsrc=["'])([^"']+)(["'][^>]*>)""", re.I)
FRONT_TITLE_RE = re.compile(r"^title:\s*['\"]?(.*?)['\"]?\s*$", re.M)
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
TEMPLATE_DELIMITER_RE = re.compile(r"({{|}}|{%|%}|{#|#})")
EVENT_TAGS = [
    ("NewStarCTF", r"newstar"),
    ("PolarCTF", r"polarctf"),
    ("BUUCTF", r"buuctf"),
    ("NSSCTF", r"nssctf"),
    ("ctfshow", r"ctfshow"),
    ("DASCTF", r"dasctf"),
    ("DIDCTF", r"didctf"),
    ("HECTF", r"hectf"),
    ("FIC", r"\bfic\b|fic决赛|fic初赛"),
    ("ISCC", r"\biscc\b"),
    ("盘古石", r"盘古石"),
    ("平航杯", r"平航"),
    ("长城杯", r"长城杯"),
    ("红明谷", r"红明谷"),
    ("春秋杯", r"春秋杯"),
    ("御网杯", r"御网杯"),
    ("数信杯", r"数信杯"),
    ("龙信杯", r"龙信杯"),
    ("Solar杯", r"solar"),
    ("SQCTF", r"sqctf|商丘"),
    ("NPCCCTF", r"npccctf"),
    ("CPPU-ISA", r"cppu-isa"),
    ("CPPU", r"cppu"),
]
TEMPLATE_ENTITIES = {
    "{{": "&#123;&#123;",
    "}}": "&#125;&#125;",
    "{%": "&#123;%",
    "%}": "%&#125;",
    "{#": "&#123;#",
    "#}": "#&#125;",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def yaml_quote(value: object) -> str:
    text = "" if value is None else str(value)
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def normalize_title(value: str) -> str:
    text = value.lower()
    text = text.replace("writeup", "wp")
    text = re.sub(r"[\s\-_:：—–~·`'\"“”‘’()（）\[\]【】<>《》/\\|,.，。!！?？]+", "", text)
    return text


def existing_titles() -> set[str]:
    titles: set[str] = set()
    for path in POSTS_DIR.glob("*.md"):
        text = read_text(path)
        match = FRONT_TITLE_RE.search(text)
        title = strip_quotes(match.group(1)) if match else path.stem
        titles.add(normalize_title(title))
    return titles


def sanitize_filename(value: str, fallback: str = "post") -> str:
    value = html.unescape(value).strip()
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", value)
    value = re.sub(r"\s+", " ", value).strip(" .")
    return (value[:100].strip(" .") or fallback)


def clean_category(value: str) -> str:
    value = str(value or "").strip()
    value = value.replace("[Markdown]", "")
    value = value.replace("[随笔分类]", "")
    return value.strip()


def add_tag(tags: list[str], tag: str) -> None:
    tag = tag.strip()
    if tag and tag not in tags:
        tags.append(tag)


def has_any(text: str, *patterns: str) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in patterns)


def classify(title: str, raw_categories: list[str], keywords: object) -> tuple[list[str], list[str]]:
    cats = [clean_category(item) for item in raw_categories]
    cats = [item for item in cats if item]
    tags: list[str] = []

    joined = title + " " + " ".join(cats)
    lower_joined = joined.lower()
    is_writeup = has_any(lower_joined, r"wp|writeup|复现|挑战赛|ctf|杯|校赛|纳新赛")
    is_forensics = has_any(lower_joined, r"取证|应急|溯源|流量|日志|恢复|fic|盘古石|长城杯|运维赛|平航|didctf|solar")

    if is_forensics and is_writeup:
        categories = ["Forensics Writeup"]
        add_tag(tags, "Forensics")
        add_tag(tags, "Writeup")
    elif "CTF Misc" in cats or "CTF-Misc" in cats:
        categories = ["CTF Misc"]
        add_tag(tags, "CTF")
        add_tag(tags, "Misc")
    elif "CTF Web" in cats or "CTF-Web" in cats:
        categories = ["CTF Web"]
        add_tag(tags, "CTF")
        add_tag(tags, "Web")
    elif "CTF Crypto" in cats or "CTF-Crypto学习" in cats:
        categories = ["CTF Crypto"]
        add_tag(tags, "CTF")
        add_tag(tags, "Crypto")
    elif "CTF Pwn" in cats or "CTF-Pwn学习" in cats:
        categories = ["CTF Pwn"]
        add_tag(tags, "CTF")
        add_tag(tags, "Pwn")
    elif "CTF-WriteUp" in cats or "比赛WP" in cats or is_writeup:
        categories = ["CTF Writeup"]
        add_tag(tags, "CTF")
        add_tag(tags, "Writeup")
    elif has_any(lower_joined, r"c\+\+|python|java|算法|数据结构|数据库|洛谷|天梯|编程|g\+\+"):
        categories = ["Programming"]
        add_tag(tags, "Programming")
    elif has_any(lower_joined, r"nmap|nessus|snort|防火墙|sql注入|弱密码|burpsuite|sqlmap|docker|wsl|kali|flask|漏洞|运维|服务器"):
        categories = ["Security Notes"]
        add_tag(tags, "Security")
    elif "周报" in joined:
        categories = ["Weekly"]
        add_tag(tags, "Weekly")
    elif has_any(joined, r"总结|年终|大一"):
        categories = ["Life"]
        add_tag(tags, "Life")
    else:
        categories = ["Others"]

    for tag, pattern in EVENT_TAGS:
        if has_any(lower_joined, pattern):
            add_tag(tags, tag)

    if has_any(lower_joined, r"misc|隐写|图片|zip|volatility|buuctf|steg"):
        add_tag(tags, "Misc")
    if has_any(lower_joined, r"pwn|ida|gdb|栈溢出|checksec|ropper"):
        add_tag(tags, "Pwn")
    if has_any(lower_joined, r"web|sql|burp|ctfshow|flask|php"):
        add_tag(tags, "Web")
    if has_any(lower_joined, r"crypto|rsa|密码|签名|序列密码|分组密码"):
        add_tag(tags, "Crypto")
    if has_any(lower_joined, r"reverse|apk|安卓|反注入|frida|ollvm|llvm"):
        add_tag(tags, "Reverse")
    if has_any(lower_joined, r"python"):
        add_tag(tags, "Python")
    if has_any(lower_joined, r"c\+\+|g\+\+"):
        add_tag(tags, "C++")
    if has_any(lower_joined, r"java|jar"):
        add_tag(tags, "Java")
    if has_any(lower_joined, r"docker|wsl|kali|linux|防火墙|snort|nmap|nessus"):
        add_tag(tags, "Linux")

    return categories, tags[:10]


def looks_like_html(content: str) -> bool:
    stripped = content.lstrip()
    return stripped.startswith("<") and bool(re.search(r"</?(p|div|h[1-6]|ul|ol|pre|table|img|br)\b", stripped, re.I))


def normalize_body(content: str) -> str:
    content = content or ""
    if looks_like_html(content) and html_to_markdown:
        content = html_to_markdown(content, heading_style="ATX")
    return protect_body(content)


def protect_body(content: str) -> str:
    return escape_template_delimiters(unwrap_raw(content).strip()) + "\n"


def unwrap_raw(content: str) -> str:
    content = content.strip()
    if content.startswith("{% raw %}") and content.endswith("{% endraw %}"):
        return content[len("{% raw %}") : -len("{% endraw %}")].strip()
    return content


def escape_template_delimiters(content: str) -> str:
    lines = content.splitlines()
    escaped: list[str] = []
    in_fence = False
    fence_marker = ""

    for line in lines:
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            escaped.append(line)
            continue
        if in_fence or line.startswith(("    ", "\t")):
            escaped.append(line)
            continue
        escaped.append(escape_inline_text(line))

    return "\n".join(escaped)


def escape_inline_text(line: str) -> str:
    result: list[str] = []
    index = 0
    while index < len(line):
        if line[index] != "`":
            next_tick = line.find("`", index)
            end = len(line) if next_tick == -1 else next_tick
            result.append(escape_template_text(line[index:end]))
            index = end
            continue

        ticks_end = index
        while ticks_end < len(line) and line[ticks_end] == "`":
            ticks_end += 1
        ticks = line[index:ticks_end]
        closing = line.find(ticks, ticks_end)
        if closing == -1:
            result.append(escape_template_text(line[index:]))
            break
        result.append(line[index : closing + len(ticks)])
        index = closing + len(ticks)
    return "".join(result)


def escape_template_text(text: str) -> str:
    return TEMPLATE_DELIMITER_RE.sub(lambda match: TEMPLATE_ENTITIES[match.group(0)], text)


def image_extension(url: str, content_type: str | None = None) -> str:
    path = urllib.parse.urlparse(url).path
    suffix = Path(urllib.parse.unquote(path)).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg", ".ico"}:
        return suffix
    content_type = (content_type or "").split(";")[0].strip().lower()
    return {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "image/bmp": ".bmp",
        "image/svg+xml": ".svg",
        "image/x-icon": ".ico",
    }.get(content_type, ".img")


def download_image(url: str, asset_dir: Path, index: int, used_names: set[str]) -> str | None:
    if not re.match(r"^https?://", url, re.I):
        return None
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.cnblogs.com/",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
            content_type = response.headers.get("Content-Type")
    except Exception as exc:
        print(f"  image download failed: {url} ({exc})")
        return None

    ext = image_extension(url, content_type)
    base = sanitize_filename(Path(urllib.parse.unquote(urllib.parse.urlparse(url).path)).stem, f"image-{index:03d}")
    filename = f"{base}{ext}"
    if filename in used_names:
        filename = f"{base}-{index:03d}{ext}"
    used_names.add(filename)

    asset_dir.mkdir(parents=True, exist_ok=True)
    dest = asset_dir / filename
    dest.write_bytes(data)
    return "/" + dest.relative_to(ROOT / "source").as_posix()


def rewrite_images(content: str, post_slug: str, dry_run: bool) -> tuple[str, int]:
    asset_dir = ASSETS_DIR / post_slug
    replacements: dict[str, str] = {}
    used_names: set[str] = set()

    def localize(url: str) -> str:
        clean = url.strip()
        if clean in replacements:
            return replacements[clean]
        if dry_run:
            replacements[clean] = clean
            return clean
        local = download_image(clean, asset_dir, len(replacements) + 1, used_names)
        replacements[clean] = local or clean
        return replacements[clean]

    def rewrite_markdown(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        if not re.match(r"^https?://", target, re.I):
            return match.group(0)
        return match.group(0).replace(match.group(1), localize(target), 1)

    def rewrite_html(match: re.Match[str]) -> str:
        target = match.group(2).strip()
        if not re.match(r"^https?://", target, re.I):
            return match.group(0)
        return f"{match.group(1)}{localize(target)}{match.group(3)}"

    content = IMAGE_MARKDOWN_RE.sub(rewrite_markdown, content)
    content = IMAGE_HTML_RE.sub(rewrite_html, content)
    downloaded = sum(1 for old, new in replacements.items() if old != new)
    return content, downloaded


def format_front_matter(data: dict[str, object], body: str) -> str:
    lines = ["---"]
    for key in ["title", "date", "categories", "tags", "cnblogs_postid", "cnblogs_url"]:
        value = data.get(key)
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {yaml_quote(item)}")
        elif key == "date":
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {yaml_quote(value)}")
    lines.append("---")
    lines.append("")
    lines.append(body.rstrip() + "\n")
    return "\n".join(lines)


def post_date(value: object) -> str:
    if isinstance(value, dt.datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if value:
        text = str(value)
        for fmt in ("%Y%m%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            try:
                return dt.datetime.strptime(text, fmt).strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass
    return time.strftime("%Y-%m-%d %H:%M:%S")


def cnblogs_url(post: dict[str, object]) -> str:
    return str(post.get("link") or post.get("permalink") or f"https://www.cnblogs.com/ljnljn/p/{post.get('postid')}.html")


def connect(user: str, token: str, blog_name: str | None) -> tuple[xmlrpc.client.ServerProxy, str]:
    endpoint = f"https://rpc.cnblogs.com/metaweblog/{blog_name or user}"
    proxy = xmlrpc.client.ServerProxy(endpoint, allow_none=True)
    blogs = proxy.blogger.getUsersBlogs("", user, token)
    if not blogs:
        raise RuntimeError("MetaWeblog did not return any blogs for this account.")
    return proxy, str(blogs[0]["blogid"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Import cnblogs MetaWeblog posts into Hexo.")
    parser.add_argument("--count", type=int, default=999)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    user = os.environ.get("CNBLOGS_USER")
    token = os.environ.get("CNBLOGS_TOKEN")
    blog_name = os.environ.get("CNBLOGS_BLOG")
    if not user or not token:
        print("Set CNBLOGS_USER and CNBLOGS_TOKEN in the environment.", file=sys.stderr)
        return 2

    proxy, blogid = connect(user, token, blog_name)
    posts = proxy.metaWeblog.getRecentPosts(blogid, user, token, args.count)
    existing = existing_titles()

    imported = 0
    skipped = 0
    downloaded_images = 0
    used_paths = {path.name.lower() for path in POSTS_DIR.glob("*.md")}

    for post in reversed(posts):
        title = str(post.get("title") or "").strip()
        if not title:
            skipped += 1
            continue
        normalized = normalize_title(title)
        if title in SKIP_TITLES or normalized in {normalize_title(item) for item in SKIP_TITLES}:
            print(f"skip protected: {title}")
            skipped += 1
            continue
        if normalized in existing:
            print(f"skip existing: {title}")
            skipped += 1
            continue

        filename_base = sanitize_filename(title, f"cnblogs-{post.get('postid')}")
        filename = f"{filename_base}.md"
        if filename.lower() in used_paths:
            filename = f"{filename_base}-{post.get('postid')}.md"
        used_paths.add(filename.lower())
        post_path = POSTS_DIR / filename

        categories, tags = classify(title, list(post.get("categories") or []), post.get("mt_keywords"))
        body = normalize_body(str(post.get("description") or ""))
        body, image_count = rewrite_images(body, sanitize_filename(title, f"cnblogs-{post.get('postid')}"), args.dry_run)
        downloaded_images += image_count
        front_matter = {
            "title": title,
            "date": post_date(post.get("dateCreated")),
            "categories": categories,
            "tags": tags,
            "cnblogs_postid": str(post.get("postid") or ""),
            "cnblogs_url": cnblogs_url(post),
        }

        if not args.dry_run:
            write_text(post_path, format_front_matter(front_matter, body))
        imported += 1
        existing.add(normalized)
        print(f"imported: {title} -> {filename} ({image_count} images)")

    print(f"summary: imported={imported}, skipped={skipped}, images={downloaded_images}, dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
