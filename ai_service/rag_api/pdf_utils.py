"""
PDF Utilities for ChiPT
Handles extraction of text from PDFs using marker-pdf (primary) or pdfplumber (fallback).
"""

import os
import tempfile
from pathlib import Path
from typing import List, Optional
import warnings

# Suppress warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

def extract_text_marker(pdf_path: str, pages: Optional[List[int]] = None) -> str:
    """
    Extract text from PDF using marker-pdf (for superior layout preservation).
    
    Args:
        pdf_path: Path to the PDF file
        pages: List of page numbers to extract (1-indexed). If None, extract all pages.
    
    Returns:
        Extracted text as Markdown string with preserved layout
    """
    try:
        # Try to use marker-pdf first
        try:
            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict
            
            # Load model (cached for subsequent calls)
            if not hasattr(extract_text_marker, 'converter'):
                print("  Loading Marker-PDF models (first time only)...")
                model_dict = create_model_dict()
                converter = PdfConverter(artifact_dict=model_dict)
                extract_text_marker.converter = converter
                print("  ✓ Marker-PDF models loaded successfully")
            
            converter = extract_text_marker.converter
            
            # Process with marker
            if pages is None:
                # Full doc
                rendered = converter(str(pdf_path))
                return rendered.markdown.strip()
            else:
                # Specific pages using temporary PDF
                import fitz
                import tempfile
                
                with pdfplumber.open(pdf_path) as pdf:
                    total_pages = len(pdf.pages)
                
                valid_pages = [p for p in pages if 1 <= p <= total_pages]
                if not valid_pages:
                    return ""
                
                src_doc = fitz.open(str(pdf_path))
                temp_pdf = fitz.open()
                for page_num in sorted(valid_pages):
                    temp_pdf.insert_pdf(src_doc, from_page=page_num - 1, to_page=page_num - 1)
                
                with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as tmp_file:
                    temp_pdf_path = tmp_file.name
                    temp_pdf.save(tmp_file.name)
                
                temp_pdf.close()
                src_doc.close()
                
                try:
                    rendered = converter(temp_pdf_path)
                    markdown_text = rendered.markdown
                    page_range = f"{valid_pages[0]}-{valid_pages[-1]}" if len(valid_pages) > 1 else str(valid_pages[0])
                    return f"*Extracted pages: {page_range}*\n\n{markdown_text}".strip()
                finally:
                    if os.path.exists(temp_pdf_path):
                        os.unlink(temp_pdf_path)

        except Exception as e:
            print(f"  Warning: Marker-PDF failed ({e}). Falling back to pdfplumber.")
            # Fallthrough to fallback
            pass

        # Fallback: pdfplumber
        import pdfplumber
        print("  Using pdfplumber fallback...")
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            pages_to_process = pages if pages else range(1, total_pages + 1)
            
            for p_num in pages_to_process:
                if 1 <= p_num <= total_pages:
                    page = pdf.pages[p_num - 1]
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
        
        return "\n\n".join(text_parts)

    except Exception as e:
        print(f"  Error extracting text from {os.path.basename(pdf_path)}: {e}")
        import traceback
        traceback.print_exc()
        return ""
