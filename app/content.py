"""Content management module for the blog."""

from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import bleach
import frontmatter
import markdown

logger = logging.getLogger(__name__)


def optimize_image_references(html_content: str) -> str:
    """Optimize image references in HTML content for better performance."""
    # Add loading="lazy" to all images for performance
    html_content = re.sub(
        r"<img([^>]*?)>", r'<img\1 loading="lazy" decoding="async">', html_content
    )

    # Add responsive image classes
    html_content = re.sub(
        r"<img([^>]*?)>", r'<img\1 class="responsive-image">', html_content
    )

    return html_content


def create_slug(filename: str) -> str:
    """Create a URL-friendly slug from a filename."""
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")

    name = Path(filename).stem
    if not name:
        raise ValueError("Filename must have a valid stem")

    slug = re.sub(r"[^\w\s-]", "", name.lower())
    slug = re.sub(r"[-\s]+", "-", slug)
    slug = slug.strip("-")

    if not slug:
        raise ValueError("Generated slug is empty")

    return slug


def validate_post_metadata(metadata: dict[str, Any], filename: str) -> dict[str, Any]:
    """Validate and sanitize post metadata."""
    validated = metadata.copy()

    # Ensure title exists and is safe
    if not validated.get("title"):
        validated["title"] = (
            Path(filename).stem.replace("-", " ").replace("_", " ").title()
        )
    elif not isinstance(validated["title"], str):
        validated["title"] = str(validated["title"])

    # Sanitize title (remove potential XSS)
    validated["title"] = re.sub(r'[<>"\']', "", validated["title"][:100])

    # Validate summary
    if validated.get("summary"):
        if not isinstance(validated["summary"], str):
            validated["summary"] = str(validated["summary"])
        validated["summary"] = validated["summary"][:500]  # Limit length

    # Validate tags
    if validated.get("tags"):
        if isinstance(validated["tags"], str):
            validated["tags"] = [tag.strip() for tag in validated["tags"].split(",")]
        elif isinstance(validated["tags"], list):
            validated["tags"] = [str(tag).strip() for tag in validated["tags"]][
                :10
            ]  # Max 10 tags
        else:
            validated["tags"] = []

    return validated


def parse_date(date_value: Any, md_file: Path) -> datetime:
    """Parse date with multiple format support and comprehensive error handling."""
    if isinstance(date_value, datetime):
        return date_value

    if isinstance(date_value, str):
        try:
            # Try ISO format first
            return datetime.fromisoformat(date_value)
        except ValueError:
            # Try common date formats
            for fmt in [
                "%Y-%m-%d",
                "%Y/%m/%d",
                "%B %d, %Y",
                "%d/%m/%Y",
                "%m/%d/%Y",
                "%Y-%m-%d %H:%M:%S",
            ]:
                try:
                    return datetime.strptime(date_value, fmt)
                except ValueError:
                    continue

            logger.warning("Could not parse date %r in %s", date_value, md_file)
            return datetime.fromtimestamp(md_file.stat().st_mtime)

    logger.error("Invalid date type in %s: %s", md_file, type(date_value))
    return datetime.fromtimestamp(md_file.stat().st_mtime)


def get_all_posts() -> list[dict[str, Any]]:
    """
    Scan the content/posts directory and return all posts sorted by date (newest first).

    Returns:
        List of dictionaries containing post metadata and slug.
    """
    posts_dir = Path("content/posts")
    posts = []

    if not posts_dir.exists():
        logger.warning("Posts directory does not exist: %s", posts_dir)
        return posts

    if not posts_dir.is_dir():
        logger.warning("Posts path is not a directory: %s", posts_dir)
        return posts

    md_files = list(posts_dir.glob("*.md"))
    if not md_files:
        logger.warning("No Markdown files found in: %s", posts_dir)
        return posts

    for md_file in md_files:
        try:
            if not md_file.is_file():
                logger.warning("Skipping non-file: %s", md_file)
                continue

            if md_file.stat().st_size == 0:
                logger.warning("Skipping empty file: %s", md_file)
                continue

            with open(md_file, encoding="utf-8") as f:
                post = frontmatter.load(f)

            # Validate and process metadata using new validation function
            metadata = validate_post_metadata(post.metadata, md_file.name)
            metadata["slug"] = create_slug(md_file.name)
            metadata["filename"] = md_file.name

            # Content metrics
            content = post.content or ""
            metadata["content"] = content
            metadata["word_count"] = len(content.split())
            metadata["read_time"] = max(1, metadata["word_count"] // 200)

            # Parse date with enhanced error handling
            if "date" in metadata:
                metadata["date"] = parse_date(metadata["date"], md_file)
            else:
                metadata["date"] = datetime.fromtimestamp(md_file.stat().st_mtime)

            posts.append(metadata)

        except FileNotFoundError:
            logger.error("File not found: %s", md_file)
            continue
        except PermissionError:
            logger.error("Permission denied reading: %s", md_file)
            continue
        except UnicodeDecodeError as e:
            logger.error("Unicode decode error in %s: %s", md_file, e)
            continue
        except frontmatter.YAMLLoadError as e:
            logger.error("YAML frontmatter error in %s: %s", md_file, e)
            continue
        except OSError as e:
            logger.error("OS error reading %s: %s", md_file, e)
            continue
        except Exception:
            logger.exception("Unexpected error loading %s", md_file)
            continue

    # Sort by date (newest first) with error handling
    try:
        posts.sort(key=lambda x: x.get("date", datetime.min), reverse=True)
    except Exception:
        logger.exception("Error sorting posts")
        # Fallback to filename sorting
        posts.sort(key=lambda x: x.get("filename", ""), reverse=True)

    logger.info("Successfully loaded %d posts from %d files", len(posts), len(md_files))
    return posts


def get_post_by_slug(slug: str) -> dict[str, Any] | None:
    """
    Retrieve a single post by its slug with enhanced error handling.

    Args:
        slug: URL-friendly identifier for the post

    Returns:
        Dictionary containing post metadata and HTML content, or None if not found.
    """
    if not slug or not isinstance(slug, str):
        logger.warning("Invalid slug provided: %s", slug)
        return None

    posts_dir = Path("content/posts")

    if not posts_dir.exists():
        logger.warning("Posts directory does not exist: %s", posts_dir)
        return None

    if not posts_dir.is_dir():
        logger.warning("Posts path is not a directory: %s", posts_dir)
        return None

    # Find the post file by matching slug
    matching_file = None
    for md_file in posts_dir.glob("*.md"):
        if create_slug(md_file.name) == slug:
            matching_file = md_file
            break

    if not matching_file:
        logger.warning("No post found with slug: %s", slug)
        return None

    try:
        if not matching_file.is_file():
            logger.warning("Path is not a file: %s", matching_file)
            return None

        if matching_file.stat().st_size == 0:
            logger.warning("Post file is empty: %s", matching_file)
            return None

        with open(matching_file, encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Validate post content
        if not post.content and not post.metadata:
            logger.warning(
                "Post file contains no content or metadata: %s", matching_file
            )
            return None

        # Configure Markdown with extensions for enhanced content processing
        try:
            md = markdown.Markdown(
                extensions=[
                    "codehilite",
                    "toc",
                    "pymdownx.superfences",
                    "pymdownx.betterem",
                    "pymdownx.tasklist",
                    "pymdownx.tilde",
                    "pymdownx.magiclink",
                    "tables",
                    "fenced_code",
                ],
                extension_configs={
                    "codehilite": {
                        "css_class": "highlight",
                        "use_pygments": True,
                        "guess_lang": False,
                        "noclasses": False,
                    },
                    "toc": {
                        "permalink": True,
                        "permalink_class": "headerlink",
                        "permalink_title": "Permalink to this headline",
                    },
                    "pymdownx.superfences": {
                        "custom_fences": [
                            {
                                "name": "mermaid",
                                "class": "mermaid",
                                "format": lambda source: f'<div class="mermaid">{source}</div>',
                            }
                        ]
                    },
                    "pymdownx.tasklist": {
                        "custom_checkbox": True,
                        "clickable_checkbox": False,
                    },
                    "pymdownx.magiclink": {
                        "repo_url_shorthand": True,
                        "social_url_shorthand": True,
                    },
                },
            )
        except Exception:
            logger.exception("Error configuring Markdown processor")
            # Fallback to basic markdown
            md = markdown.Markdown()

        # Convert content to HTML with error handling
        try:
            html_content = md.convert(post.content or "")
        except Exception as e:
            logger.error("Error converting markdown to HTML for %s: %s", slug, e)
            html_content = f"<p>Error processing content: {e}</p>"

        allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union(
            {
                "p",
                "pre",
                "span",
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "img",
                "table",
                "thead",
                "tbody",
                "tr",
                "th",
                "td",
                "code",
                "blockquote",
                "ul",
                "ol",
                "li",
                "div",
            }
        )
        allowed_attributes = {
            **bleach.sanitizer.ALLOWED_ATTRIBUTES,
            "img": ["src", "alt", "title", "loading", "decoding", "class"],
            "a": ["href", "title", "rel"],
            "*": ["class"],
        }
        html_content = bleach.clean(
            html_content, tags=allowed_tags, attributes=allowed_attributes
        )

        # Optimize image references for performance
        html_content = optimize_image_references(html_content)

        # Validate and process metadata using new validation function
        metadata = validate_post_metadata(post.metadata or {}, matching_file.name)

        content_text = post.content or ""
        metadata["word_count"] = len(content_text.split())
        metadata["read_time"] = max(1, metadata["word_count"] // 200)

        # Parse date with enhanced error handling
        if "date" in metadata:
            metadata["date"] = parse_date(metadata["date"], matching_file)
        else:
            metadata["date"] = datetime.fromtimestamp(matching_file.stat().st_mtime)

        result = {
            "slug": slug,
            "content": html_content,
            "toc": getattr(md, "toc", ""),
            **metadata,
        }

        logger.info("Successfully loaded post: %s", slug)
        return result

    except FileNotFoundError:
        logger.error("Post file not found: %s", matching_file)
        return None
    except PermissionError:
        logger.error("Permission denied reading post: %s", matching_file)
        return None
    except UnicodeDecodeError as e:
        logger.error("Unicode decode error in post %s: %s", slug, e)
        return None
    except frontmatter.YAMLLoadError as e:
        logger.error("YAML frontmatter error in post %s: %s", slug, e)
        return None
    except OSError as e:
        logger.error("OS error reading post %s: %s", slug, e)
        return None
    except Exception:
        logger.exception("Unexpected error loading post %s", slug)
        return None
