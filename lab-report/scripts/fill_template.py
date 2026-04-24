#!/usr/bin/env python3
"""Template filling with docxtpl, CJK support, and de-AI styles."""

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

try:
    from docx import Document
    from docxtpl import DocxTemplate
    from docx.oxml.ns import qn
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

# De-AI banned words
BANNED_WORDS = ['首先', '其次', '最后', '总而言之', '值得注意的是', '综上所述', '不可否认']

def set_cjk_font(run, font_name='宋体'):
    """Set CJK font for a run to prevent tofu."""
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)

def apply_de_ai_style(text: str) -> str:
    """Apply de-AI style to text."""
    # This is a placeholder - actual de-AI would be done by the AI agent
    # We just verify no banned words exist
    for word in BANNED_WORDS:
        if word in text:
            print(f"Warning: Found banned AI word '{word}' in content", file=sys.stderr)
    return text

def fill_template(template_path: Path, data_path: Path, output_path: Path, style: str = "normal"):
    """Fill template with data."""
    if not HAS_DOCX:
        return {"error": "Missing dependencies: python-docx, docxtpl"}
    
    result = {
        "success": False,
        "template": str(template_path),
        "output": str(output_path),
        "placeholders_filled": [],
        "placeholders_missing": [],
        "style_applied": style
    }
    
    try:
        # Load data
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Copy template (never modify original)
        shutil.copy(template_path, output_path)
        
        # Load and render template
        doc = DocxTemplate(output_path)
        
        # Render with Jinja2 context
        doc.render(data)
        
        # Save
        doc.save(output_path)
        
        # Verify CJK fonts
        verify_doc = Document(output_path)
        for para in verify_doc.paragraphs:
            for run in para.runs:
                if any('\u4e00' <= c <= '\u9fff' for c in run.text):
                    set_cjk_font(run)
        verify_doc.save(output_path)
        
        result["success"] = True
        
        # Check for unreplaced placeholders
        final_doc = Document(output_path)
        full_text = " ".join([p.text for p in final_doc.paragraphs])
        import re
        remaining = re.findall(r'\{\{([^}]+)\}\}', full_text)
        result["placeholders_missing"] = remaining
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

def verify_original_unchanged(template_path: Path, original_hash: str) -> bool:
    """Verify original template wasn't modified."""
    with open(template_path, 'rb') as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()
    return current_hash == original_hash

def main():
    parser = argparse.ArgumentParser(description='Fill DOCX template')
    parser.add_argument('--template', '-t', required=True, help='Template DOCX file')
    parser.add_argument('--data', '-d', required=True, help='JSON data file')
    parser.add_argument('--output', '-o', required=True, help='Output DOCX file')
    parser.add_argument('--style', '-s', choices=['perfect', 'normal'], default='normal',
                       help='Report style (both use de-AI guidelines)')
    args = parser.parse_args()
    
    template_path = Path(args.template)
    data_path = Path(args.data)
    output_path = Path(args.output)
    
    if not template_path.exists():
        print(f"Error: Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)
    
    if not data_path.exists():
        print(f"Error: Data file not found: {data_path}", file=sys.stderr)
        sys.exit(1)
    
    # Get original hash before any operation
    with open(template_path, 'rb') as f:
        original_hash = hashlib.sha256(f.read()).hexdigest()
    
    result = fill_template(template_path, data_path, output_path, args.style)
    
    # Verify original unchanged
    if not verify_original_unchanged(template_path, original_hash):
        print("Error: Original template was modified!", file=sys.stderr)
        sys.exit(1)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("success") else 1)

if __name__ == '__main__':
    main()
