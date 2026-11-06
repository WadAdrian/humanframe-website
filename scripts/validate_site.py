#!/usr/bin/env python3
"""Check this static website without installing packages or contacting a server.

Run from any directory with ``python3 /path/to/scripts/validate_site.py``.
An optional positional directory allows checks against a copied export.
This checks source integrity; browser QA is still needed for visual layout.
"""

from __future__ import annotations

import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET


ORIGIN = "https://humanframerobotics.com"
CONTACT_EMAIL = "hello@humanframerobotics.com"
PRIMARY_ROUTES = (
    "/", "/robot/", "/features/", "/research/", "/framework/", "/why-humanframe/",
    "/applications/reminiscence/", "/team/", "/contact/",
)
SUPPORTING_ROUTES = ("/alp/", "/technology/", "/developers/", "/platform/", "/about/")
PUBLIC_ROUTES = PRIMARY_ROUTES + SUPPORTING_ROUTES
TEAM_PROFILES = {
    "adrian-wadhwa.webp": ("Adrian Wadhwa", "CEO"),
    "jacob-camoin.webp": ("Jacob Camoin", "CTO"),
    "rudy-arsenault.webp": ("Rudy Arsenault", "Head of Robotics"),
    "theron-boozer.webp": ("Theron Boozer", "Head of Hardware and Mechatronics"),
}
SOCIAL_FIELDS = (
    "og:type", "og:site_name", "og:title", "og:description", "og:url", "og:image", "og:image:alt",
    "twitter:card", "twitter:title", "twitter:description", "twitter:image", "twitter:image:alt",
)
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
CSS_URL = re.compile(r"url\(\s*(?P<quote>['\"]?)(?P<url>.*?)\1\s*\)", re.IGNORECASE)
INTERNAL_TERMS = re.compile(
    r"Raspberry\s*Pi|\bCM5\b|\bSSH\b|\bFlask\b|\bUSB\b|\blocalhost\b|127\.0\.0\.1|\bports?\s+\d{2,5}\b",
    re.IGNORECASE,
)


def route_for(path: Path, root: Path) -> str:
    relative = path.relative_to(root).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return "/" + relative.removesuffix("index.html")
    return "/" + relative


class Page(HTMLParser):
    def __init__(self, path: Path, root: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.route = route_for(path, root)
        self.ids: Counter[str] = Counter()
        self.tags: Counter[str] = Counter()
        self.meta: dict[str, list[str]] = {}
        self.canonicals: list[str] = []
        self.references: list[tuple[str, str, int]] = []
        self.images: list[tuple[dict[str, str | None], int]] = []
        self.primary_links: set[str] = set()
        self.footer_links: set[str] = set()
        self.elements: list[tuple[str, dict[str, str | None], int, tuple[str, ...]]] = []
        self.inquiry_controls: list[tuple[str, dict[str, str | None], int, bool]] = []
        self.visible_text: list[tuple[str, int]] = []
        self.team_profiles: list[tuple[list[str], list[str]]] = []
        self.memory_grids = 0
        self.memory_prompts = 0
        self.title: list[str] = []
        self.stack: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attributes = dict(attributes)
        line = self.getpos()[0]
        self.tags[tag] += 1
        self.elements.append((tag, attributes, line, tuple(item[0] for item in self.stack)))
        if tag == "article" and "team-card" in (attributes.get("class") or "").split():
            self.team_profiles.append(([], []))
        if "memory-grid" in (attributes.get("class") or "").split():
            self.memory_grids += 1
        if tag in {"li", "div"} and self.stack and "memory-grid" in (self.stack[-1][1].get("class") or "").split():
            self.memory_prompts += 1
        if tag in {"input", "select", "textarea"} and any(
            item_tag == "form" and "data-inquiry-form" in item_attrs
            for item_tag, item_attrs in self.stack
        ):
            self.inquiry_controls.append((tag, attributes, line, any(item[0] == "label" for item in self.stack)))
        if attributes.get("id"):
            self.ids[attributes["id"]] += 1
        if tag == "meta":
            key = attributes.get("name") or attributes.get("property")
            if key:
                self.meta.setdefault(key.lower(), []).append(attributes.get("content") or "")
        if tag == "link" and "canonical" in (attributes.get("rel") or "").split():
            self.canonicals.append(attributes.get("href") or "")
        for name in ("href", "src", "poster"):
            if name in attributes:
                self.references.append((attributes[name] or "", f"{tag}[{name}]", line))
        if "srcset" in attributes:
            # The repository uses ordinary local image candidates, not data URLs.
            for candidate in (attributes["srcset"] or "").split(","):
                if candidate.strip():
                    self.references.append((candidate.strip().split()[0], f"{tag}[srcset]", line))
        if tag == "img":
            self.images.append((attributes, line))
            if self.team_profiles and any(
                item_tag == "article" and "team-card" in (item_attrs.get("class") or "").split()
                for item_tag, item_attrs in self.stack
            ):
                self.team_profiles[-1][0].append(attributes.get("src") or "")
        if tag == "a" and any(
            item_tag == "nav" and item_attrs.get("aria-label") == "Primary navigation"
            for item_tag, item_attrs in self.stack
        ):
            self.primary_links.add(attributes.get("href") or "")
        if tag == "a" and any(item_tag == "footer" for item_tag, _ in self.stack):
            self.footer_links.add(attributes.get("href") or "")
        if tag not in VOID_TAGS:
            self.stack.append((tag, attributes))

    def handle_startendtag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attributes)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if any(tag == "title" for tag, _ in self.stack):
            self.title.append(data)
        if data.strip() and not any(tag in {"head", "script", "style", "template"} for tag, _ in self.stack):
            self.visible_text.append((data, self.getpos()[0]))
        if self.team_profiles and any(
            tag == "article" and "team-card" in (attributes.get("class") or "").split()
            for tag, attributes in self.stack
        ):
            self.team_profiles[-1][1].append(data)


def raster_size(path: Path) -> tuple[int, int] | None:
    """Read dimensions used by this site's WebP assets with the standard library."""
    data = path.read_bytes()
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        offset = 12
        while offset + 8 <= len(data):
            chunk = data[offset:offset + 4]
            length = int.from_bytes(data[offset + 4:offset + 8], "little")
            payload = data[offset + 8:offset + 8 + length]
            if chunk == b"VP8X" and len(payload) >= 10:
                return (1 + int.from_bytes(payload[4:7], "little"), 1 + int.from_bytes(payload[7:10], "little"))
            if chunk == b"VP8 " and len(payload) >= 10 and payload[3:6] == b"\x9d\x01\x2a":
                return (int.from_bytes(payload[6:8], "little") & 0x3FFF, int.from_bytes(payload[8:10], "little") & 0x3FFF)
            if chunk == b"VP8L" and len(payload) >= 5 and payload[0] == 0x2F:
                bits = int.from_bytes(payload[1:5], "little")
                return (1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF))
            offset += 8 + length + (length % 2)
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    return None


class Validator:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.errors: list[str] = []
        self.pages: dict[Path, Page] = {}
        self.references_checked = 0
        self.images_checked = 0

    def error(self, path: Path, message: str, line: int | None = None) -> None:
        location = path.relative_to(self.root).as_posix()
        if line is not None:
            location += f":{line}"
        self.errors.append(f"{location}: {message}")

    def local_target(self, source: Path, reference: str) -> tuple[Path | None, str]:
        base = ORIGIN + (self.pages[source].route if source in self.pages else "/" + source.relative_to(self.root).as_posix())
        url = urlsplit(urljoin(base, reference))
        if url.scheme not in ("http", "https") or url.netloc != urlsplit(ORIGIN).netloc:
            return None, ""
        candidate = (self.root / unquote(url.path).lstrip("/")).resolve()
        if not candidate.is_relative_to(self.root):
            return candidate, url.fragment
        if candidate.is_dir():
            candidate = candidate / "index.html"
        return candidate, unquote(url.fragment)

    def check_reference(self, source: Path, reference: str, context: str, line: int | None = None) -> None:
        self.references_checked += 1
        if not reference.strip() or reference == "#":
            self.error(source, f"empty or placeholder {context}", line)
            return
        reference_path = unquote(urlsplit(reference).path).lower()
        if any(folder in reference_path for folder in ("assets/media/humanoid/", "assets/media/research/")) or Path(reference_path).name.startswith("alp-humanoid-"):
            self.error(source, f"superseded product artwork in {context}: {reference}", line)
        scheme = urlsplit(reference).scheme.lower()
        if scheme in ("javascript", "vbscript"):
            self.error(source, f"executable URL in {context}", line)
            return
        if scheme == "mailto":
            if not re.fullmatch(r"[^@\s?]+@[^@\s?]+\.[^@\s?]+", urlsplit(reference).path):
                self.error(source, f"invalid email destination {reference!r}", line)
            return
        target, fragment = self.local_target(source, reference)
        if target is None:
            return
        if not target.is_relative_to(self.root) or not target.is_file():
            self.error(source, f"missing local {context}: {reference}", line)
        elif fragment and target in self.pages and fragment not in self.pages[target].ids:
            self.error(source, f"missing fragment #{fragment} in {target.relative_to(self.root)}", line)

    def check_page(self, page: Page) -> None:
        path = page.path
        for tag in ("main", "h1", "title"):
            if page.tags[tag] != 1:
                self.error(path, f"expected one <{tag}>, found {page.tags[tag]}")
        if not "".join(page.title).strip():
            self.error(path, "empty page title")
        for identifier, count in page.ids.items():
            if count > 1:
                self.error(path, f"duplicate id {identifier!r} ({count} occurrences)")
        missing_navigation = set(PRIMARY_ROUTES) - page.primary_links
        if missing_navigation:
            self.error(path, "primary navigation is missing " + ", ".join(sorted(missing_navigation)))
        missing_footer = set(SUPPORTING_ROUTES) - page.footer_links
        if missing_footer:
            self.error(path, "footer is missing preserved routes " + ", ".join(sorted(missing_footer)))
        for text, line in page.visible_text:
            match = INTERNAL_TERMS.search(text)
            if match:
                self.error(path, f"implementation detail in public copy: {match.group()!r}", line)
        if page.route in PUBLIC_ROUTES:
            for field in ("description",) + SOCIAL_FIELDS:
                values = page.meta.get(field, [])
                if len(values) != 1 or not values[0].strip():
                    self.error(path, f"expected one nonempty {field} meta tag")
            canonical = ORIGIN + page.route
            if page.canonicals != [canonical]:
                self.error(path, f"canonical must be {canonical}")
            if page.meta.get("og:url") != [canonical]:
                self.error(path, "og:url must match the canonical URL")
            if page.meta.get("twitter:card") != ["summary_large_image"]:
                self.error(path, "twitter:card must be summary_large_image")
        elif page.route == "/404.html" and "noindex" not in ",".join(page.meta.get("robots", [])):
            self.error(path, "404 page must have robots noindex")
        for field in ("og:image", "twitter:image"):
            for reference in page.meta.get(field, []):
                self.check_reference(path, reference, field)
        for reference, context, line in page.references:
            self.check_reference(path, reference, context, line)
        for image, line in page.images:
            self.images_checked += 1
            if "alt" not in image:
                self.error(path, "image is missing alt text (use alt=\"\" for decorative images)", line)
            dimensions = []
            for attribute in ("width", "height"):
                value = image.get(attribute) or ""
                if not value.isdigit() or int(value) <= 0:
                    self.error(path, f"image {attribute} must be a positive integer", line)
                else:
                    dimensions.append(int(value))
            target, _ = self.local_target(path, image.get("src") or "")
            if len(dimensions) == 2 and target is not None and target.is_file():
                intrinsic = raster_size(target)
                if intrinsic is not None and tuple(dimensions) != intrinsic:
                    self.error(path, f"image dimensions {tuple(dimensions)} do not match {target.name}: {intrinsic}", line)

    def check_research_inquiry(self) -> None:
        contact = next((page for page in self.pages.values() if page.route == "/contact/"), None)
        research = next((page for page in self.pages.values() if page.route == "/research/"), None)
        if contact is None or research is None:
            return  # Missing public pages are reported by run().
        destination = "/contact/?interest=research#research-inquiry"
        if not any(reference == destination for reference, _, _ in research.references):
            self.error(research.path, "research page needs a contextual collaboration CTA")
        if "research-inquiry" not in contact.ids:
            self.error(contact.path, "research inquiry fragment is missing")
        forms = [(tag, attrs, line) for tag, attrs, line, _ in contact.elements if "data-inquiry-form" in attrs]
        if len(forms) != 1 or forms[0][0] != "form":
            self.error(contact.path, "expected one email-preparation form")
            return
        _, form, line = forms[0]
        if "hidden" not in form or form.get("action"):
            self.error(contact.path, "email-preparation form must wait for JavaScript and must not submit to an endpoint", line)
        controls = {attrs.get("name"): (tag, attrs, number, wrapped) for tag, attrs, number, wrapped in contact.inquiry_controls}
        expected = {"name": "input", "email": "input", "institution": "input", "interest": "select", "message": "textarea"}
        for name, expected_tag in expected.items():
            if name not in controls:
                self.error(contact.path, f"inquiry form is missing {name}")
                continue
            tag, attributes, number, wrapped = controls[name]
            if tag != expected_tag or "required" not in attributes:
                self.error(contact.path, f"inquiry {name} must be a required {expected_tag}", number)
            explicit_label = any(
                element_tag == "label" and attributes.get("id") and element_attrs.get("for") == attributes["id"]
                for element_tag, element_attrs, _, _ in contact.elements
            )
            if not wrapped and not explicit_label:
                self.error(contact.path, f"inquiry {name} needs a visible associated label", number)
        if "email" in controls and controls["email"][1].get("type") != "email":
            self.error(contact.path, "inquiry email must use type=email")
        topics = {
            attrs.get("value") for tag, attrs, _, parents in contact.elements
            if tag == "option" and "select" in parents
        }
        if not {"", "Research collaboration"}.issubset(topics):
            self.error(contact.path, "inquiry topic select needs its prompt and research collaboration option")
        for marker, expected_tag in (("data-inquiry-preview", "section"), ("data-inquiry-body", "pre"), ("data-inquiry-email", "a")):
            matches = [(tag, attrs) for tag, attrs, _, _ in contact.elements if marker in attrs]
            if len(matches) != 1 or matches[0][0] != expected_tag:
                self.error(contact.path, f"email preparation needs one {expected_tag}[{marker}]")
            elif marker == "data-inquiry-email" and matches[0][1].get("href") != f"mailto:{CONTACT_EMAIL}":
                self.error(contact.path, "email draft destination must match the published contact address")
        if not any(reference == f"mailto:{CONTACT_EMAIL}" for reference, _, _ in contact.references):
            self.error(contact.path, "contact page needs a direct email fallback")

    def check_team_and_application(self) -> None:
        team = next((page for page in self.pages.values() if page.route == "/team/"), None)
        if team is not None:
            expected = {f"/assets/media/team/{filename}" for filename in TEAM_PROFILES}
            portraits = [attrs.get("src") or "" for attrs, _ in team.images if "/assets/media/team/" in (attrs.get("src") or "")]
            if Counter(portraits) != Counter(expected):
                self.error(team.path, "team page must show each of the four supplied portraits exactly once")
            if len(team.team_profiles) != 4:
                self.error(team.path, "team page needs four associated name, role and portrait profiles")
            for images, text in team.team_profiles:
                if len(images) != 1 or images[0] not in expected:
                    self.error(team.path, "each team profile needs one supplied portrait")
                    continue
                name, role = TEAM_PROFILES[Path(images[0]).name]
                label = " ".join(" ".join(text).split())
                if name not in label or role not in label:
                    self.error(team.path, f"portrait {Path(images[0]).name} needs its correct name and role")
        application = next((page for page in self.pages.values() if page.route == "/applications/reminiscence/"), None)
        if application is not None:
            if application.memory_grids != 1 or application.memory_prompts != 9:
                self.error(application.path, "reminiscence page needs one native nine-prompt illustrative selection grid")
            text = " ".join(" ".join(value for value, _ in application.visible_text).split()).lower()
            if "illustrative" not in text or "pepper" not in text or "adaptation" not in text or not any(status in text for status in ("in development", "in progress")):
                self.error(application.path, "reminiscence page must distinguish its illustrative interaction, prior Pepper work and developing HumanFrame adaptation")

    def check_sitemap(self) -> None:
        path = self.root / "sitemap.xml"
        try:
            tree = ET.parse(path)
        except (OSError, ET.ParseError) as error:
            self.error(path, f"cannot read sitemap: {error}")
            return
        locations = [element.text or "" for element in tree.findall(".//{*}loc")]
        if Counter(locations) != Counter(ORIGIN + route for route in PUBLIC_ROUTES):
            self.error(path, "sitemap must contain each public canonical URL exactly once")
        for location in locations:
            self.check_reference(path, location, "sitemap URL")
        robots = self.root / "robots.txt"
        try:
            text = robots.read_text(encoding="utf-8")
        except OSError as error:
            self.error(robots, f"cannot read robots.txt: {error}")
            return
        if f"Sitemap: {ORIGIN}/sitemap.xml" not in text:
            self.error(robots, "missing canonical sitemap reference")

    def check_vercel(self) -> None:
        path = self.root / "vercel.json"
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            self.error(path, f"cannot read Vercel configuration: {error}")
            return
        if config.get("rewrites") or config.get("routes"):
            self.error(path, "static site must preserve native file and 404 routing")
        global_headers = {
            header["key"].lower(): header["value"]
            for rule in config.get("headers", []) if rule.get("source") == "/(.*)"
            for header in rule.get("headers", [])
        }
        # Keep the existing host-independent policy and Vercel configuration aligned.
        headers_path = self.root / "_headers"
        try:
            block = headers_path.read_text(encoding="utf-8").split("\n\n", 1)[0]
        except OSError as error:
            self.error(headers_path, f"cannot read security headers: {error}")
            return
        for line in block.splitlines()[1:]:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                if global_headers.get(key.lower()) != value.strip():
                    self.error(path, f"{key} does not match _headers")

    def run(self) -> int:
        for path in sorted(self.root.rglob("*.html")):
            if any(part.startswith(".") for part in path.relative_to(self.root).parts):
                continue
            page = Page(path, self.root)
            page.feed(path.read_text(encoding="utf-8"))
            self.pages[path] = page
        for route in PUBLIC_ROUTES:
            if not any(page.route == route for page in self.pages.values()):
                self.error(self.root / "index.html", f"missing public route {route}")
        for page in self.pages.values():
            self.check_page(page)
        self.check_research_inquiry()
        self.check_team_and_application()
        stylesheets = list((self.root / "assets").rglob("*.css"))
        for path in stylesheets:
            content = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
            for match in CSS_URL.finditer(content):
                self.check_reference(path, match.group("url").strip(), "CSS asset")
        self.check_sitemap()
        self.check_vercel()
        if self.errors:
            print(f"FAIL: {len(self.errors)} issue(s)")
            for error in self.errors:
                print(f"  {error}")
            return 1
        print(f"PASS: {len(self.pages)} HTML pages, {len(stylesheets)} stylesheets, {self.images_checked} images, {self.references_checked} references.")
        print("Checked local links, fragments, assets, navigation, image dimensions, SEO/social metadata, inquiry form, team labels, reminiscence illustration, sitemap and static hosting policy; no superseded product artwork or public implementation jargon.")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    arguments = parser.parse_args()
    if not arguments.root.is_dir():
        parser.error(f"site directory does not exist: {arguments.root}")
    return Validator(arguments.root).run()


if __name__ == "__main__":
    sys.exit(main())
