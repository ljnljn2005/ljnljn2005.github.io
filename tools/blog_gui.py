from __future__ import annotations

import html
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext
import tkinter as tk
from tkinter import ttk


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source"
FRIENDS_FILE = SOURCE_DIR / "friends" / "index.md"
ABOUT_FILE = SOURCE_DIR / "about" / "index.md"
POSTS_DIR = SOURCE_DIR / "_posts"
SOURCE_ASSETS_DIR = SOURCE_DIR / "assets"
POST_ASSETS_DIR = POSTS_DIR / "assets"
FRIEND_ASSET_DIR = SOURCE_ASSETS_DIR / "friends"
NPM = "npm.cmd" if os.name == "nt" else "npm"
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\n]+)\)")
HTML_IMAGE_RE = re.compile(r"""(<img\b[^>]*\bsrc=["'])([^"']+)(["'][^>]*>)""", re.I)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def split_front_matter(content: str) -> tuple[dict[str, object], str]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, content

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, content

    data: dict[str, object] = {}
    current_key: str | None = None
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        item_match = re.match(r"^\s*-\s*(.*)$", raw)
        if item_match and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(strip_quotes(item_match.group(1)))
            continue

        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", raw)
        if not match:
            current_key = None
            continue
        key, value = match.group(1), (match.group(2) or "")
        current_key = key
        value = value.strip()
        if value == "":
            data[key] = []
        elif value == "[]":
            data[key] = []
        elif value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
        else:
            data[key] = strip_quotes(value)

    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    return data, body


def yaml_quote(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    text = "" if value is None else str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def normalize_list_text(text: str) -> list[str]:
    parts = re.split(r"[,，\n]", text)
    return [part.strip() for part in parts if part.strip()]


def format_front_matter(data: dict[str, object], body: str, key_order: list[str] | None = None) -> str:
    key_order = key_order or ["title", "date", "categories", "tags", "comment", "comments"]
    keys = [key for key in key_order if key in data]
    keys.extend(key for key in data.keys() if key not in keys)

    lines = ["---"]
    for key in keys:
        value = data[key]
        if isinstance(value, list):
            if value:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: []")
        elif key == "date":
            lines.append(f"{key}: {value}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        else:
            lines.append(f"{key}: {yaml_quote(value)}")
    lines.append("---")
    lines.append("")
    lines.append(body.rstrip() + "\n")
    return "\n".join(lines)


def slugify(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or f"friend-{int(time.time())}"


def is_local_asset(value: str) -> bool:
    return value.startswith("/assets/friends/") or value.startswith("assets/friends/")


def import_avatar(source: str, name: str) -> str:
    source = source.strip()
    if not source or is_local_asset(source):
        return source

    FRIEND_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    dest = FRIEND_ASSET_DIR / f"{slugify(name)}.webp"

    if re.match(r"^https?://", source, re.I):
        request = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            data = response.read()
        tmp = FRIEND_ASSET_DIR / f".{dest.stem}.download"
        tmp.write_bytes(data)
        input_path = tmp
    else:
        input_path = Path(source).expanduser()
        if not input_path.is_absolute():
            input_path = (ROOT / input_path).resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"头像文件不存在：{input_path}")
        tmp = None

    try:
        try:
            from PIL import Image, ImageOps

            with Image.open(input_path) as image:
                image = image.convert("RGBA")
                image = ImageOps.fit(image, (192, 192), method=Image.Resampling.LANCZOS)
                image.save(dest, "WEBP", quality=86, method=6)
        except Exception:
            fallback = dest.with_suffix(input_path.suffix or ".img")
            shutil.copyfile(input_path, fallback)
            return "/" + fallback.relative_to(ROOT / "source").as_posix()
    finally:
        if tmp and tmp.exists():
            tmp.unlink()

    return "/" + dest.relative_to(ROOT / "source").as_posix()


def is_external_target(target: str) -> bool:
    return bool(re.match(r"^(?:[a-z][a-z0-9+.-]*:)?//|^(?:data|mailto|tel|javascript):", target, re.I))


def split_target_suffix(target: str) -> tuple[str, str]:
    indexes = [idx for idx in (target.find("?"), target.find("#")) if idx >= 0]
    if not indexes:
        return target, ""
    idx = min(indexes)
    return target[:idx], target[idx:]


def unwrap_image_target(target: str) -> str:
    value = target.strip()
    if len(value) >= 2 and value[0] == "<" and value[-1] == ">":
        return value[1:-1].strip()
    return value


def decode_local_target(target: str) -> str:
    base, suffix = split_target_suffix(unwrap_image_target(target))
    decoded = urllib.parse.unquote(base).replace("\\", "/").strip()
    while decoded.startswith("./"):
        decoded = decoded[2:]
    return decoded + suffix


def encode_local_target(target: str) -> str:
    return target.replace(" ", "%20")


def normalize_image_target(post_path: Path, target: str) -> str:
    original = unwrap_image_target(target)
    if not original or is_external_target(original):
        return target

    base, suffix = split_target_suffix(original)
    decoded = urllib.parse.unquote(base).replace("\\", "/").strip()
    while decoded.startswith("./"):
        decoded = decoded[2:]

    public_path: str | None = None
    if decoded.startswith("/assets/"):
        public_path = decoded
    elif decoded.startswith("assets/"):
        public_path = "/" + decoded
    elif decoded.startswith("_posts/assets/"):
        public_path = "/" + decoded.removeprefix("_posts/")
    elif decoded.startswith("source/_posts/assets/"):
        public_path = "/" + decoded.removeprefix("source/_posts/")
    elif decoded.startswith("/source/_posts/assets/"):
        public_path = "/" + decoded.removeprefix("/source/_posts/")
    else:
        candidate = (post_path.parent / decoded).resolve()
        if candidate.exists() and candidate.is_file():
            public_path = f"/assets/{post_path.stem}/{candidate.name}"

    if not public_path:
        return target
    return encode_local_target(public_path + suffix)


def public_target_to_source_path(target: str) -> Path | None:
    base, _suffix = split_target_suffix(unwrap_image_target(target))
    decoded = urllib.parse.unquote(base).replace("\\", "/").strip()
    if not decoded.startswith("/assets/"):
        return None
    return SOURCE_DIR / decoded.lstrip("/")


def image_source_candidates(post_path: Path, original_target: str, public_target: str) -> list[Path]:
    candidates: list[Path] = []
    original = decode_local_target(original_target)
    original_base, _suffix = split_target_suffix(original)
    public_base, _public_suffix = split_target_suffix(decode_local_target(public_target))

    for raw in [original_base, public_base.lstrip("/")]:
        if not raw:
            continue
        clean = raw.lstrip("/")
        candidates.extend(
            [
                SOURCE_DIR / clean,
                POSTS_DIR / clean,
                post_path.parent / clean,
            ]
        )
        if clean.startswith("assets/"):
            candidates.append(POST_ASSETS_DIR / clean.removeprefix("assets/"))

    unique: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved not in seen:
            unique.append(resolved)
            seen.add(resolved)
    return unique


def iter_image_targets(content: str) -> list[str]:
    targets = [match.group(1).strip() for match in MARKDOWN_IMAGE_RE.finditer(content)]
    targets.extend(match.group(2).strip() for match in HTML_IMAGE_RE.finditer(content))
    return targets


def analyze_post_health(post_path: Path) -> tuple[list[str], int]:
    content = read_text(post_path)
    issues: list[str] = []
    fixable = 0

    if content.startswith("\ufeff"):
        issues.append("文件开头包含 UTF-8 BOM，可能影响 front matter 识别。")
        fixable += 1
    if not content.lstrip("\ufeff").startswith("---"):
        issues.append("缺少 Hexo front matter。")

    targets = iter_image_targets(content)
    if not targets:
        issues.append("未检测到图片引用。")

    for target in targets:
        clean = unwrap_image_target(target)
        if not clean or is_external_target(clean):
            continue
        normalized = normalize_image_target(post_path, target)
        if normalized != target:
            issues.append(f"图片引用建议改为站点绝对路径：{target} -> {normalized}")
            fixable += 1

        public_target = normalized if normalized.startswith("/assets/") else target
        source_path = public_target_to_source_path(public_target)
        if source_path and not source_path.exists():
            candidate = next((item for item in image_source_candidates(post_path, target, public_target) if item.exists()), None)
            if candidate:
                issues.append(f"图片尚未发布，可从 {candidate} 复制到 {source_path}")
                fixable += 1
            else:
                issues.append(f"图片文件不存在：{public_target}")

    return issues, fixable


def fix_post_health(post_path: Path) -> list[str]:
    content = read_text(post_path)
    changes: list[str] = []
    if content.startswith("\ufeff"):
        content = content.lstrip("\ufeff")
        changes.append("移除 UTF-8 BOM")

    def fix_target(target: str) -> str:
        normalized = normalize_image_target(post_path, target)
        if normalized != target:
            changes.append(f"修正图片路径：{target} -> {normalized}")

        source_path = public_target_to_source_path(normalized)
        if source_path and not source_path.exists():
            candidate = next((item for item in image_source_candidates(post_path, target, normalized) if item.exists()), None)
            if candidate:
                source_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(candidate, source_path)
                changes.append(f"复制图片：{candidate} -> {source_path}")
        return normalized

    content = MARKDOWN_IMAGE_RE.sub(lambda match: match.group(0).replace(match.group(1), fix_target(match.group(1)), 1), content)
    content = HTML_IMAGE_RE.sub(lambda match: f"{match.group(1)}{fix_target(match.group(2))}{match.group(3)}", content)

    if changes:
        write_text(post_path, content)
    return changes


@dataclass
class Friend:
    group: str
    name: str
    url: str
    avatar: str
    bio: str


def parse_friends() -> list[Friend]:
    if not FRIENDS_FILE.exists():
        return []

    friends: list[Friend] = []
    current_group = "默认"
    lines = read_text(FRIENDS_FILE).splitlines()
    i = 0
    while i < len(lines):
        group_match = re.search(r"<h2>(.*?)</h2>", lines[i])
        if group_match:
            current_group = html.unescape(group_match.group(1).strip())
            i += 1
            continue

        if '<div class="friend-card">' not in lines[i]:
            i += 1
            continue

        block = [lines[i]]
        i += 1
        while i < len(lines):
            block.append(lines[i])
            if lines[i].startswith("    </div>"):
                break
            i += 1
        text = "\n".join(block)
        url = re.search(r'class="friend-avatar-link"\s+href="([^"]*)"', text)
        avatar = re.search(r'<img\s+src="([^"]*)"', text)
        name = re.search(r'<div class="friend-name"><a[^>]*>(.*?)</a></div>', text, re.S)
        bio = re.search(r'<div class="friend-bio">(.*?)</div>', text, re.S)
        if name:
            friends.append(
                Friend(
                    group=current_group,
                    name=html.unescape(re.sub(r"<.*?>", "", name.group(1)).strip()),
                    url=html.unescape(url.group(1).strip()) if url else "",
                    avatar=html.unescape(avatar.group(1).strip()) if avatar else "",
                    bio=html.unescape(re.sub(r"<.*?>", "", bio.group(1)).strip()) if bio else "",
                )
            )
        i += 1
    return friends


def friend_card(friend: Friend) -> str:
    name = html.escape(friend.name, quote=True)
    url = html.escape(friend.url, quote=True)
    avatar = html.escape(friend.avatar, quote=True)
    bio = html.escape(friend.bio, quote=False)
    return f"""    <div class="friend-card">
      <a class="friend-avatar-link" href="{url}" rel="noopener noreferrer" target="_blank">
        <img src="{avatar}" alt="{name}" class="friend-avatar" onerror="this.style.display='none'" />
      </a>
      <div class="friend-name"><a href="{url}" rel="noopener noreferrer" target="_blank">{name}</a></div>
      <div class="friend-bio">{bio}</div>
    </div>"""


def write_friends(friends: list[Friend]) -> None:
    groups: list[str] = []
    for friend in friends:
        if friend.group not in groups:
            groups.append(friend.group)

    body_lines = [
        "{% raw %}",
        '<div class="friend-links-page">',
        '  <p class="friend-links-intro"><strong>非常感谢师傅们的陪伴与支持！</strong></p>',
        "",
    ]
    for group in groups:
        body_lines.append(f"  <h2>{html.escape(group)}</h2>")
        body_lines.append('  <div class="friend-links-container">')
        for friend in [item for item in friends if item.group == group]:
            body_lines.append(friend_card(friend))
            body_lines.append("")
        if body_lines[-1] == "":
            body_lines.pop()
        body_lines.append("  </div>")
        body_lines.append("")
    body_lines.append("</div>")
    body_lines.append("{% endraw %}")

    data = {
        "title": "友链",
        "date": "2026-05-25 19:58:00",
        "comment": False,
        "comments": False,
    }
    write_text(FRIENDS_FILE, format_front_matter(data, "\n".join(body_lines)))


class BlogGui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ljnljn 博客管理器")
        self.geometry("1120x760")
        self.minsize(960, 650)

        self.friends: list[Friend] = []
        self.post_paths: list[Path] = []
        self.current_post: Path | None = None
        self.server_process: subprocess.Popen[str] | None = None
        self.post_check_after_id: str | None = None

        self._build_ui()
        self.reload_friends()
        self.load_about()
        self.reload_posts()

    def _build_ui(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.friend_tab = ttk.Frame(notebook)
        self.about_tab = ttk.Frame(notebook)
        self.posts_tab = ttk.Frame(notebook)
        self.deploy_tab = ttk.Frame(notebook)

        notebook.add(self.friend_tab, text="友链")
        notebook.add(self.about_tab, text="关于")
        notebook.add(self.posts_tab, text="文章标签")
        notebook.add(self.deploy_tab, text="构建部署")

        self._build_friend_tab()
        self._build_about_tab()
        self._build_posts_tab()
        self._build_deploy_tab()

    def _build_friend_tab(self) -> None:
        pane = ttk.PanedWindow(self.friend_tab, orient=tk.HORIZONTAL)
        pane.pack(fill="both", expand=True, padx=8, pady=8)

        left = ttk.Frame(pane)
        right = ttk.Frame(pane)
        pane.add(left, weight=3)
        pane.add(right, weight=2)

        columns = ("group", "name", "bio", "url")
        self.friend_tree = ttk.Treeview(left, columns=columns, show="headings", height=18)
        for key, title, width in [
            ("group", "分组", 80),
            ("name", "名称", 150),
            ("bio", "描述", 210),
            ("url", "链接", 260),
        ]:
            self.friend_tree.heading(key, text=title)
            self.friend_tree.column(key, width=width, anchor="w")
        self.friend_tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(left, orient=tk.VERTICAL, command=self.friend_tree.yview)
        scroll.pack(side="right", fill="y")
        self.friend_tree.configure(yscrollcommand=scroll.set)
        self.friend_tree.bind("<<TreeviewSelect>>", self.on_friend_select)

        form = ttk.LabelFrame(right, text="友链信息")
        form.pack(fill="x", padx=8, pady=8)
        self.friend_group = tk.StringVar()
        self.friend_name = tk.StringVar()
        self.friend_url = tk.StringVar()
        self.friend_avatar = tk.StringVar()
        self.friend_bio = tk.StringVar()

        self.friend_group_combo = ttk.Combobox(form, textvariable=self.friend_group, values=["校内", "校外"])
        self._form_row(form, "分组", self.friend_group_combo)
        self._form_row(form, "名称", ttk.Entry(form, textvariable=self.friend_name))
        self._form_row(form, "链接", ttk.Entry(form, textvariable=self.friend_url))

        avatar_row = ttk.Frame(form)
        avatar_entry = ttk.Entry(avatar_row, textvariable=self.friend_avatar)
        avatar_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(avatar_row, text="选择", command=self.choose_avatar).pack(side="left", padx=(6, 0))
        self._form_row(form, "头像", avatar_row)
        self._form_row(form, "描述", ttk.Entry(form, textvariable=self.friend_bio))

        buttons = ttk.Frame(right)
        buttons.pack(fill="x", padx=8, pady=4)
        ttk.Button(buttons, text="新增空白", command=self.new_friend).pack(side="left", padx=4)
        ttk.Button(buttons, text="保存/更新", command=self.save_friend).pack(side="left", padx=4)
        ttk.Button(buttons, text="删除选中", command=self.delete_friend).pack(side="left", padx=4)
        ttk.Button(buttons, text="重新加载", command=self.reload_friends).pack(side="left", padx=4)

        tip = ttk.Label(
            right,
            text="头像可填网址或本地文件。保存时会自动缓存到 source/assets/friends/，避免外链失效。",
            wraplength=360,
            foreground="#666",
        )
        tip.pack(fill="x", padx=12, pady=8)

    def _build_about_tab(self) -> None:
        frame = ttk.Frame(self.about_tab)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        top = ttk.Frame(frame)
        top.pack(fill="x")
        ttk.Label(top, text="标题").pack(side="left")
        self.about_title = tk.StringVar()
        ttk.Entry(top, textvariable=self.about_title, width=40).pack(side="left", padx=8)
        ttk.Button(top, text="保存关于页", command=self.save_about).pack(side="left", padx=4)
        ttk.Button(top, text="重新加载", command=self.load_about).pack(side="left", padx=4)

        self.about_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Consolas", 11))
        self.about_text.pack(fill="both", expand=True, pady=(10, 0))

    def _build_posts_tab(self) -> None:
        pane = ttk.PanedWindow(self.posts_tab, orient=tk.HORIZONTAL)
        pane.pack(fill="both", expand=True, padx=8, pady=8)

        left = ttk.Frame(pane)
        right = ttk.Frame(pane)
        pane.add(left, weight=2)
        pane.add(right, weight=3)

        self.post_tree = ttk.Treeview(left, columns=("title", "date"), show="headings")
        self.post_tree.heading("title", text="文章")
        self.post_tree.heading("date", text="日期")
        self.post_tree.column("title", width=250, anchor="w")
        self.post_tree.column("date", width=140, anchor="w")
        self.post_tree.pack(side="left", fill="both", expand=True)
        post_scroll = ttk.Scrollbar(left, orient=tk.VERTICAL, command=self.post_tree.yview)
        post_scroll.pack(side="right", fill="y")
        self.post_tree.configure(yscrollcommand=post_scroll.set)
        self.post_tree.bind("<<TreeviewSelect>>", self.on_post_select)

        form = ttk.LabelFrame(right, text="文章 Front Matter")
        form.pack(fill="x", padx=8, pady=8)
        self.post_title = tk.StringVar()
        self.post_date = tk.StringVar()
        self._form_row(form, "标题", ttk.Entry(form, textvariable=self.post_title))
        self._form_row(form, "日期", ttk.Entry(form, textvariable=self.post_date))

        ttk.Label(right, text="分类（逗号或换行分隔）").pack(anchor="w", padx=12, pady=(8, 2))
        self.post_categories = scrolledtext.ScrolledText(right, height=4, wrap=tk.WORD)
        self.post_categories.pack(fill="x", padx=8)

        ttk.Label(right, text="标签（逗号或换行分隔）").pack(anchor="w", padx=12, pady=(8, 2))
        self.post_tags = scrolledtext.ScrolledText(right, height=5, wrap=tk.WORD)
        self.post_tags.pack(fill="x", padx=8)

        buttons = ttk.Frame(right)
        buttons.pack(fill="x", padx=8, pady=10)
        ttk.Button(buttons, text="保存文章信息", command=self.save_post).pack(side="left", padx=4)
        ttk.Button(buttons, text="重新扫描文章", command=self.reload_posts).pack(side="left", padx=4)

        self.post_path_label = ttk.Label(right, text="", foreground="#666", wraplength=540)
        self.post_path_label.pack(fill="x", padx=12, pady=8)

        check_frame = ttk.LabelFrame(right, text="文章健康检查")
        check_frame.pack(fill="both", expand=True, padx=8, pady=(4, 8))
        check_row = ttk.Frame(check_frame)
        check_row.pack(fill="x", padx=8, pady=6)
        ttk.Label(check_row, text="MD 文件名").pack(side="left")
        self.post_check_name = tk.StringVar()
        check_entry = ttk.Entry(check_row, textvariable=self.post_check_name, width=34)
        check_entry.pack(side="left", fill="x", expand=True, padx=6)
        check_entry.bind("<KeyRelease>", self.schedule_post_check)
        check_entry.bind("<Return>", self.check_post_now)
        ttk.Button(check_row, text="检测", command=self.check_post_now).pack(side="left", padx=3)
        ttk.Button(check_row, text="一键修复", command=self.fix_checked_post).pack(side="left", padx=3)

        self.post_check_output = scrolledtext.ScrolledText(check_frame, height=8, wrap=tk.WORD, font=("Consolas", 10))
        self.post_check_output.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _build_deploy_tab(self) -> None:
        frame = ttk.Frame(self.deploy_tab)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        controls = ttk.LabelFrame(frame, text="构建与部署")
        controls.pack(fill="x")

        ttk.Label(controls, text="提交信息").pack(side="left", padx=(8, 4), pady=8)
        self.commit_message = tk.StringVar(value="Update blog content")
        ttk.Entry(controls, textvariable=self.commit_message, width=36).pack(side="left", padx=4)
        ttk.Button(controls, text="构建", command=lambda: self.run_commands([[NPM, "run", "build"]])).pack(side="left", padx=4)
        ttk.Button(controls, text="Git 状态", command=lambda: self.run_commands([["git", "status", "--short", "--branch"]])).pack(side="left", padx=4)
        ttk.Button(controls, text="提交并推送", command=self.commit_and_push).pack(side="left", padx=4)
        ttk.Button(controls, text="构建+提交+推送", command=self.build_commit_push).pack(side="left", padx=4)

        preview = ttk.LabelFrame(frame, text="预览")
        preview.pack(fill="x", pady=(10, 0))
        ttk.Button(preview, text="启动本地预览", command=self.start_preview).pack(side="left", padx=8, pady=8)
        ttk.Button(preview, text="打开本地友链", command=lambda: webbrowser.open("http://localhost:4000/friends/")).pack(side="left", padx=4)
        ttk.Button(preview, text="打开线上博客", command=lambda: webbrowser.open("https://ljnljn2005.github.io/")).pack(side="left", padx=4)

        self.log_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=24, font=("Consolas", 10))
        self.log_text.pack(fill="both", expand=True, pady=(10, 0))

    def _form_row(self, parent: ttk.Frame, label: str, widget: tk.Widget) -> None:
        row = ttk.Frame(parent)
        row.pack(fill="x", padx=8, pady=5)
        ttk.Label(row, text=label, width=8).pack(side="left")
        widget.pack(side="left", fill="x", expand=True)

    def reload_friends(self) -> None:
        self.friends = parse_friends()
        self.friend_tree.delete(*self.friend_tree.get_children())
        for idx, friend in enumerate(self.friends):
            self.friend_tree.insert("", "end", iid=str(idx), values=(friend.group, friend.name, friend.bio, friend.url))
        groups = sorted({friend.group for friend in self.friends} | {"校内", "校外"})
        self.friend_group_combo.configure(values=groups)

    def on_friend_select(self, _event: tk.Event) -> None:
        selection = self.friend_tree.selection()
        if not selection:
            return
        friend = self.friends[int(selection[0])]
        self.friend_group.set(friend.group)
        self.friend_name.set(friend.name)
        self.friend_url.set(friend.url)
        self.friend_avatar.set(friend.avatar)
        self.friend_bio.set(friend.bio)

    def new_friend(self) -> None:
        self.friend_tree.selection_remove(self.friend_tree.selection())
        self.friend_group.set("校内")
        self.friend_name.set("")
        self.friend_url.set("")
        self.friend_avatar.set("")
        self.friend_bio.set("")

    def choose_avatar(self) -> None:
        filename = filedialog.askopenfilename(
            title="选择头像",
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp;*.bmp;*.ico;*.gif"), ("All files", "*.*")],
        )
        if filename:
            self.friend_avatar.set(filename)

    def save_friend(self) -> None:
        try:
            name = self.friend_name.get().strip()
            if not name:
                messagebox.showwarning("缺少名称", "友链名称不能为空。")
                return
            avatar = import_avatar(self.friend_avatar.get().strip(), name)
            friend = Friend(
                group=self.friend_group.get().strip() or "默认",
                name=name,
                url=self.friend_url.get().strip(),
                avatar=avatar,
                bio=self.friend_bio.get().strip(),
            )
            selection = self.friend_tree.selection()
            if selection:
                self.friends[int(selection[0])] = friend
            else:
                self.friends.append(friend)
            write_friends(self.friends)
            self.reload_friends()
            messagebox.showinfo("已保存", "友链已保存。")
        except Exception as exc:
            messagebox.showerror("保存失败", str(exc))

    def delete_friend(self) -> None:
        selection = self.friend_tree.selection()
        if not selection:
            return
        idx = int(selection[0])
        if not messagebox.askyesno("确认删除", f"删除友链：{self.friends[idx].name}？"):
            return
        del self.friends[idx]
        write_friends(self.friends)
        self.reload_friends()

    def load_about(self) -> None:
        data, body = split_front_matter(read_text(ABOUT_FILE))
        self.about_title.set(str(data.get("title", "关于")))
        self.about_text.delete("1.0", tk.END)
        self.about_text.insert("1.0", body)

    def save_about(self) -> None:
        data, _body = split_front_matter(read_text(ABOUT_FILE))
        data["title"] = self.about_title.get().strip() or "关于"
        if "date" not in data:
            data["date"] = time.strftime("%Y-%m-%d %H:%M:%S")
        body = self.about_text.get("1.0", tk.END).rstrip() + "\n"
        write_text(ABOUT_FILE, format_front_matter(data, body))
        messagebox.showinfo("已保存", "关于页已保存。")

    def reload_posts(self) -> None:
        self.post_paths = sorted(POSTS_DIR.glob("*.md"), key=lambda path: path.name.lower())
        self.post_tree.delete(*self.post_tree.get_children())
        for idx, path in enumerate(self.post_paths):
            data, _body = split_front_matter(read_text(path))
            title = str(data.get("title", path.stem))
            date = str(data.get("date", ""))
            self.post_tree.insert("", "end", iid=str(idx), values=(title, date))

    def on_post_select(self, _event: tk.Event) -> None:
        selection = self.post_tree.selection()
        if not selection:
            return
        self.current_post = self.post_paths[int(selection[0])]
        data, _body = split_front_matter(read_text(self.current_post))
        self.post_title.set(str(data.get("title", self.current_post.stem)))
        self.post_date.set(str(data.get("date", "")))
        self.post_categories.delete("1.0", tk.END)
        self.post_categories.insert("1.0", "\n".join(data.get("categories", []) if isinstance(data.get("categories"), list) else [str(data.get("categories", ""))]))
        self.post_tags.delete("1.0", tk.END)
        self.post_tags.insert("1.0", "\n".join(data.get("tags", []) if isinstance(data.get("tags"), list) else [str(data.get("tags", ""))]))
        self.post_path_label.configure(text=str(self.current_post))
        self.post_check_name.set(self.current_post.name)
        self.check_post_now()

    def save_post(self) -> None:
        if not self.current_post:
            messagebox.showwarning("未选择文章", "请先选择一篇文章。")
            return
        data, body = split_front_matter(read_text(self.current_post))
        data["title"] = self.post_title.get().strip() or self.current_post.stem
        data["date"] = self.post_date.get().strip()
        data["categories"] = normalize_list_text(self.post_categories.get("1.0", tk.END))
        data["tags"] = normalize_list_text(self.post_tags.get("1.0", tk.END))
        write_text(self.current_post, format_front_matter(data, body))
        self.reload_posts()
        messagebox.showinfo("已保存", "文章信息已保存。")

    def schedule_post_check(self, _event: tk.Event | None = None) -> None:
        if self.post_check_after_id:
            self.after_cancel(self.post_check_after_id)
        if not self.post_check_name.get().strip():
            self.set_post_check_output("")
            return
        self.post_check_after_id = self.after(650, self.check_post_now)

    def set_post_check_output(self, text: str) -> None:
        self.post_check_output.delete("1.0", tk.END)
        self.post_check_output.insert("1.0", text)

    def resolve_post_from_check_input(self) -> Path:
        query = self.post_check_name.get().strip().strip('"')
        if not query:
            if self.current_post:
                return self.current_post
            raise ValueError("请输入 MD 文件名，或先在左侧选择一篇文章。")

        candidate = Path(query)
        if candidate.is_absolute() and candidate.exists():
            return candidate

        names = {query}
        if not query.lower().endswith(".md"):
            names.add(f"{query}.md")
        for name in names:
            exact = POSTS_DIR / name
            if exact.exists():
                return exact

        lower_query = query.lower().removesuffix(".md")
        matches: list[Path] = []
        for path in self.post_paths or sorted(POSTS_DIR.glob("*.md")):
            data, _body = split_front_matter(read_text(path))
            title = str(data.get("title", path.stem)).lower()
            if lower_query in path.stem.lower() or lower_query in path.name.lower() or lower_query in title:
                matches.append(path)

        if len(matches) == 1:
            return matches[0]
        if not matches:
            raise ValueError(f"没有找到文章：{query}")
        preview = "\n".join(f"- {path.name}" for path in matches[:8])
        raise ValueError(f"匹配到多篇文章，请输入更完整的文件名：\n{preview}")

    def check_post_now(self, _event: tk.Event | None = None) -> None:
        self.post_check_after_id = None
        try:
            post_path = self.resolve_post_from_check_input()
            issues, fixable = analyze_post_health(post_path)
            lines = [f"检查文章：{post_path.name}", f"路径：{post_path}"]
            if issues:
                lines.append("")
                lines.append(f"发现 {len(issues)} 个问题，其中 {fixable} 个可一键修复：")
                lines.extend(f"- {issue}" for issue in issues)
            else:
                lines.append("")
                lines.append("未发现明显问题。")
            self.set_post_check_output("\n".join(lines))
        except Exception as exc:
            self.set_post_check_output(f"检测失败：{exc}")

    def fix_checked_post(self) -> None:
        try:
            post_path = self.resolve_post_from_check_input()
            changes = fix_post_health(post_path)
            issues, fixable = analyze_post_health(post_path)
            self.reload_posts()
            lines = [f"修复文章：{post_path.name}", f"路径：{post_path}", ""]
            if changes:
                lines.append(f"已执行 {len(changes)} 项修复：")
                lines.extend(f"- {change}" for change in changes)
            else:
                lines.append("没有可执行的自动修复。")
            lines.append("")
            if issues:
                lines.append(f"复查仍有 {len(issues)} 个问题，其中 {fixable} 个可自动修复：")
                lines.extend(f"- {issue}" for issue in issues)
            else:
                lines.append("复查通过，未发现明显问题。")
            self.set_post_check_output("\n".join(lines))
        except Exception as exc:
            messagebox.showerror("修复失败", str(exc))

    def append_log(self, text: str) -> None:
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)

    def run_commands(self, commands: list[list[str]]) -> None:
        def worker() -> None:
            for command in commands:
                self.after(0, self.append_log, f"\n$ {' '.join(command)}\n")
                try:
                    process = subprocess.Popen(
                        command,
                        cwd=ROOT,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        shell=False,
                    )
                    assert process.stdout is not None
                    for line in process.stdout:
                        self.after(0, self.append_log, line)
                    code = process.wait()
                    self.after(0, self.append_log, f"[exit {code}]\n")
                    if code != 0:
                        break
                except Exception as exc:
                    self.after(0, self.append_log, f"命令失败：{exc}\n")
                    break

        threading.Thread(target=worker, daemon=True).start()

    def commit_and_push(self) -> None:
        message = self.commit_message.get().strip() or "Update blog content"
        self.run_commands(
            [
                ["git", "add", "--", "source", "_config.yml", "_config.redefine.yml", "package.json", "README.md", "tools", "run-blog-gui.bat"],
                ["git", "commit", "-m", message],
                ["git", "push"],
            ]
        )

    def build_commit_push(self) -> None:
        message = self.commit_message.get().strip() or "Update blog content"
        self.run_commands(
            [
                [NPM, "run", "build"],
                ["git", "add", "--", "source", "_config.yml", "_config.redefine.yml", "package.json", "README.md", "tools", "run-blog-gui.bat"],
                ["git", "commit", "-m", message],
                ["git", "push"],
            ]
        )

    def start_preview(self) -> None:
        if self.server_process and self.server_process.poll() is None:
            webbrowser.open("http://localhost:4000/")
            return
        self.append_log("\n$ npm run server\n")
        self.server_process = subprocess.Popen(
            [NPM, "run", "server"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
        )

        def reader() -> None:
            if not self.server_process or not self.server_process.stdout:
                return
            for line in self.server_process.stdout:
                self.after(0, self.append_log, line)

        threading.Thread(target=reader, daemon=True).start()
        self.after(1600, lambda: webbrowser.open("http://localhost:4000/"))


if __name__ == "__main__":
    if not ROOT.exists():
        print("Cannot locate blog root.", file=sys.stderr)
        sys.exit(1)
    app = BlogGui()
    app.mainloop()
