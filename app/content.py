"""Content management module for the blog."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import frontmatter
import markdown

if TYPE_CHECKING:
    pass


def create_slug(filename: str) -> str:
    """Create a URL-friendly slug from a filename."""
    name = Path(filename).stem
    slug = re.sub(r"[^\w\s-]", "", name.lower())
    slug = re.sub(r"[-\s]+", "-", slug)
    return slug.strip("-")


def get_all_posts() -> list[dict[str, Any]]:
    """
    Scan the content/posts directory and return all posts sorted by date (newest first).

    Returns:
        List of dictionaries containing post metadata and slug.
    """
    posts_dir = Path("content/posts")
    posts = []

    if not posts_dir.exists():
        print(f"Posts directory does not exist: {posts_dir}")
        return posts

    if not posts_dir.is_dir():
        print(f"Posts path is not a directory: {posts_dir}")
        return posts

    md_files = list(posts_dir.glob("*.md"))
    if not md_files:
        print(f"No Markdown files found in: {posts_dir}")
        return posts

    for md_file in md_files:
        try:
            if not md_file.is_file():
                print(f"Skipping non-file: {md_file}")
                continue

            if md_file.stat().st_size == 0:
                print(f"Skipping empty file: {md_file}")
                continue

            with open(md_file, encoding="utf-8") as f:
                post = frontmatter.load(f)

            # Extract metadata with validation
            metadata = post.metadata.copy()
            metadata["slug"] = create_slug(md_file.name)
            metadata["filename"] = md_file.name

            # Validate required fields
            if not metadata.get("title"):
                metadata["title"] = (
                    md_file.stem.replace("-", " ").replace("_", " ").title()
                )

            # Parse date with multiple format support
            if "date" in metadata:
                if isinstance(metadata["date"], str):
                    try:
                        # Try ISO format first
                        metadata["date"] = datetime.fromisoformat(metadata["date"])
                    except ValueError:
                        try:
                            # Try common date formats
                            for fmt in [
                                "%Y-%m-%d",
                                "%Y/%m/%d",
                                "%B %d, %Y",
                                "%d/%m/%Y",
                            ]:
                                try:
                                    metadata["date"] = datetime.strptime(
                                        metadata["date"], fmt
                                    )
                                    break
                                except ValueError:
                                    continue
                            else:
                                print(
                                    f"Could not parse date '{metadata['date']}' in {md_file}"
                                )
                                metadata["date"] = datetime.now()
                        except Exception:
                            metadata["date"] = datetime.now()
                elif not isinstance(metadata["date"], datetime):
                    print(f"Invalid date type in {md_file}: {type(metadata['date'])}")
                    metadata["date"] = datetime.now()
            else:
                # Use file modification time as fallback
                metadata["date"] = datetime.fromtimestamp(md_file.stat().st_mtime)

            posts.append(metadata)

        except FileNotFoundError:
            print(f"File not found: {md_file}")
            continue
        except PermissionError:
            print(f"Permission denied reading: {md_file}")
            continue
        except UnicodeDecodeError as e:
            print(f"Unicode decode error in {md_file}: {e}")
            continue
        except frontmatter.YAMLLoadError as e:
            print(f"YAML frontmatter error in {md_file}: {e}")
            continue
        except OSError as e:
            print(f"OS error reading {md_file}: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error loading {md_file}: {e}")
            continue

    # Sort by date (newest first) with error handling
    try:
        posts.sort(key=lambda x: x.get("date", datetime.min), reverse=True)
    except Exception as e:
        print(f"Error sorting posts: {e}")
        # Fallback to filename sorting
        posts.sort(key=lambda x: x.get("filename", ""), reverse=True)

    print(f"Successfully loaded {len(posts)} posts from {len(md_files)} files")
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
        print(f"Invalid slug provided: {slug}")
        return None

    posts_dir = Path("content/posts")

    if not posts_dir.exists():
        print(f"Posts directory does not exist: {posts_dir}")
        return None

    if not posts_dir.is_dir():
        print(f"Posts path is not a directory: {posts_dir}")
        return None

    # Find the post file by matching slug
    matching_file = None
    for md_file in posts_dir.glob("*.md"):
        if create_slug(md_file.name) == slug:
            matching_file = md_file
            break

    if not matching_file:
        print(f"No post found with slug: {slug}")
        return None

    try:
        if not matching_file.is_file():
            print(f"Path is not a file: {matching_file}")
            return None

        if matching_file.stat().st_size == 0:
            print(f"Post file is empty: {matching_file}")
            return None

        with open(matching_file, encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Validate post content
        if not post.content and not post.metadata:
            print(f"Post file contains no content or metadata: {matching_file}")
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
        except Exception as e:
            print(f"Error configuring Markdown processor: {e}")
            # Fallback to basic markdown
            md = markdown.Markdown()

        # Convert content to HTML with error handling
        try:
            html_content = md.convert(post.content or "")
        except Exception as e:
            print(f"Error converting markdown to HTML for {slug}: {e}")
            html_content = f"<p>Error processing content: {e}</p>"

        # Process metadata with validation
        metadata = post.metadata.copy() if post.metadata else {}

        # Ensure title exists
        if not metadata.get("title"):
            metadata["title"] = (
                matching_file.stem.replace("-", " ").replace("_", " ").title()
            )

        # Parse date with multiple format support
        if "date" in metadata:
            if isinstance(metadata["date"], str):
                try:
                    # Try ISO format first
                    metadata["date"] = datetime.fromisoformat(metadata["date"])
                except ValueError:
                    try:
                        # Try common date formats
                        for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%B %d, %Y", "%d/%m/%Y"]:
                            try:
                                metadata["date"] = datetime.strptime(
                                    metadata["date"], fmt
                                )
                                break
                            except ValueError:
                                continue
                        else:
                            print(
                                f"Could not parse date '{metadata['date']}' in {matching_file}"
                            )
                            metadata["date"] = datetime.fromtimestamp(
                                matching_file.stat().st_mtime
                            )
                    except Exception:
                        metadata["date"] = datetime.fromtimestamp(
                            matching_file.stat().st_mtime
                        )
            elif not isinstance(metadata["date"], datetime):
                print(f"Invalid date type in {matching_file}: {type(metadata['date'])}")
                metadata["date"] = datetime.fromtimestamp(matching_file.stat().st_mtime)
        else:
            # Use file modification time as fallback
            metadata["date"] = datetime.fromtimestamp(matching_file.stat().st_mtime)

        result = {
            "slug": slug,
            "content": html_content,
            "toc": getattr(md, "toc", ""),
            **metadata,
        }

        print(f"Successfully loaded post: {slug}")
        return result

    except FileNotFoundError:
        print(f"Post file not found: {matching_file}")
        return None
    except PermissionError:
        print(f"Permission denied reading post: {matching_file}")
        return None
    except UnicodeDecodeError as e:
        print(f"Unicode decode error in post {slug}: {e}")
        return None
    except frontmatter.YAMLLoadError as e:
        print(f"YAML frontmatter error in post {slug}: {e}")
        return None
    except OSError as e:
        print(f"OS error reading post {slug}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error loading post {slug}: {e}")
        return None
