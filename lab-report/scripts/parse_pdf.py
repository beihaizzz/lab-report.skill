#!/usr/bin/env python3
"""PDF text extraction and scanned detection."""

import argparse
import json
import sys
from pathlib import Path

try:
    import pdfplumber
    import pymupdf4llm
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

try:
    import pytesseract
    from pdf2image import convert_from_path
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

def parse_pdf(filepath: Path, output_format: str = "json", ocr: bool = False):
    """Parse PDF and extract text."""
    if not HAS_DEPS:
        return {"error": "Missing dependencies: pdfplumber, pymupdf4llm"}
    
    result = {
        "filename": filepath.name,
        "page_count": 0,
        "text_by_page": [],
        "markdown": "",
        "is_scanned": False,
        "warning": None
    }
    
    try:
        # Extract with pdfplumber
        with pdfplumber.open(filepath) as pdf:
            result["page_count"] = len(pdf.pages)
            
            total_text = ""
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                result["text_by_page"].append({
                    "page": i + 1,
                    "content": text
                })
                total_text += text + "\n"
            
            # Check if scanned (no extractable text)
            if not total_text.strip():
                if ocr and HAS_OCR:
                    # Attempt OCR for scanned PDFs
                    try:
                        images = convert_from_path(str(filepath))
                        result["text_by_page"] = []
                        total_text = ""
                        for i, img in enumerate(images):
                            page_text = pytesseract.image_to_string(img, lang='chi_sim+eng')
                            result["text_by_page"].append({
                                "page": i + 1,
                                "content": page_text
                            })
                            total_text += page_text + "\n"
                        result["is_scanned"] = False
                        result["warning"] = "OCR_USED"
                    except Exception as e:
                        result["is_scanned"] = True
                        result["warning"] = f"OCR_FAILED: {e}"
                elif ocr and not HAS_OCR:
                    result["is_scanned"] = True
                    result["warning"] = "OCR_DEPS_MISSING"
                else:
                    result["is_scanned"] = True
                    result["warning"] = "SCANNED_PDF_DETECTED"
        
        # Convert to markdown with pymupdf4llm
        try:
            result["markdown"] = pymupdf4llm.to_markdown(str(filepath))
        except Exception as e:
            # 降级：用普通文本拼接作为 markdown
            fallback_lines = []
            for page in result.get("text_by_page", []):
                fallback_lines.append(f"## 第 {page['page']} 页\n\n{page['content']}")
            result["markdown"] = "\n\n".join(fallback_lines) if fallback_lines else ""
            result["warning"] = (result.get("warning") or "") + f" Markdown转换失败({type(e).__name__})，已降级为纯文本"
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

def main():
    parser = argparse.ArgumentParser(description='Parse PDF file')
    parser.add_argument('--input', '-i', required=True, help='Input PDF file')
    parser.add_argument('--format', '-f', choices=['json', 'markdown'], default='json')
    parser.add_argument('--ocr', action='store_true', help='Enable OCR for scanned PDFs')
    args = parser.parse_args()
    
    filepath = Path(args.input)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    
    result = parse_pdf(filepath, args.format, ocr=args.ocr)
    
    if args.format == "markdown":
        print(result.get("markdown", ""))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    sys.exit(0 if "error" not in result else 1)

if __name__ == '__main__':
    main()
