#!/usr/bin/env python3
"""PPTX text extraction — uses markitdown instead of python-pptx."""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from markitdown import MarkItDown
    HAS_MARKITDOWN = True
except ImportError:
    HAS_MARKITDOWN = False


def parse_pptx(filepath: Path, output_format: str = "json"):
    """Parse PPTX and extract text from all slides using markitdown."""
    if not HAS_MARKITDOWN:
        return {"error": "Missing dependency: markitdown"}

    result = {
        "filename": filepath.name,
        "slide_count": 0,
        "slides": []
    }

    try:
        md = MarkItDown()
        md_result = md.convert(str(filepath))
        md_text = md_result.text_content

        # Parse markdown into slides structure
        # markitdown outputs: <!-- Slide number: N --> then content
        lines = md_text.split('\n')
        current_slide = None
        for line in lines:
            # Match <!-- Slide number: N --> markers
            slide_match = re.match(r'^<!--\s*Slide\s+number:\s*(\d+)\s*-->', line, re.IGNORECASE)
            if slide_match:
                if current_slide:
                    result["slides"].append(current_slide)
                current_slide = {
                    "number": len(result["slides"]) + 1,
                    "title": "",
                    "content": []
                }
                continue
            if current_slide is None:
                # First lines before any slide marker are treated as intro
                continue
            if current_slide and line.strip():
                # First non-empty content after slide header becomes title
                if not current_slide["title"]:
                    current_slide["title"] = line.strip()
                else:
                    current_slide["content"].append(line.strip())

        if current_slide:
            result["slides"].append(current_slide)

        result["slide_count"] = len(result["slides"])

    except Exception as e:
        result["error"] = str(e)

    return result


def to_markdown(result: dict) -> str:
    """Convert result to markdown format."""
    lines = [f"# {result['filename']}\n"]
    for slide in result.get("slides", []):
        lines.append(f"## Slide {slide['number']}")
        if slide.get("title"):
            lines.append(f"**{slide['title']}**\n")
        for content in slide.get("content", []):
            lines.append(content)
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Parse PPTX file')
    parser.add_argument('--input', '-i', required=True, help='Input PPTX file')
    parser.add_argument('--format', '-f', choices=['json', 'markdown'], default='json')
    args = parser.parse_args()

    filepath = Path(args.input)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    result = parse_pptx(filepath, args.format)

    if args.format == "markdown":
        if "error" in result:
            print(f"# Error: {result['error']}")
            sys.exit(1)
        print(to_markdown(result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    sys.exit(0 if "error" not in result else 1)


if __name__ == '__main__':
    main()