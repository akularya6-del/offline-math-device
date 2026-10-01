import os
import fitz  # PyMuPDF

pdf_path = "data/real_cuet/cuet_paper.pdf"
out_dir = "data/real_cuet/pages"
os.makedirs(out_dir, exist_ok=True)

def extract_pages():
    try:
        doc = fitz.open(pdf_path)
        print(f"Extracting {len(doc)} pages...")
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=300)
            img_path = os.path.join(out_dir, f"page_{page_num+1:02d}.png")
            pix.save(img_path)
        print("Extraction complete.")
    except Exception as e:
        print(f"Failed to extract PDF: {e}")

if __name__ == "__main__":
    extract_pages()
