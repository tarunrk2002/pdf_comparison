import fitz  # PyMuPDF


def extract_fonts(pdf_path):
    """Extract fonts and their properties from a PDF."""
    doc = fitz.open(pdf_path)
    font_info = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text_instances = page.get_text("dict")["blocks"]

        for instance in text_instances:
            if "lines" in instance:
                for line in instance["lines"]:
                    for span in line["spans"]:
                        font_info.append({
                            "text": span["text"],
                            "font": span["font"],
                            "size": span["size"],
                            "page": page_num + 1
                        })
    return font_info


def compare_fonts(pdf1_fonts, pdf2_fonts):
    """Compare the fonts between two PDFs and return the differences."""
    differences = []

    for i, (font1, font2) in enumerate(zip(pdf1_fonts, pdf2_fonts)):
        
        if font1["font"] != font2["font"] or font1["size"] != font2["size"]:
            differences.append({
                "pdf1_text": font1["text"],
                "pdf2_text": font2["text"],
                "pdf1_font": font1["font"],
                "pdf2_font": font2["font"],
                "pdf1_size": font1["size"],
                "pdf2_size": font2["size"],
                "page": font1["page"]
            })

    return differences


def show_differences(differences):
    """Display the differences between the two PDFs."""
    for diff in differences:
        print(f"Page {diff['page']}:")
        print(f"  PDF1 -> Text: '{diff['pdf1_text']}' | Font: {diff['pdf1_font']} | Size: {diff['pdf1_size']}")
        print(f"  PDF2 -> Text: '{diff['pdf2_text']}' | Font: {diff['pdf2_font']} | Size: {diff['pdf2_size']}")
        print("-" * 50)


# Paths to your PDFs
pdf1_path = "pdf1.pdf"
pdf2_path = "pdf2.pdf"

# Extract fonts from both PDFs
pdf1_fonts = extract_fonts(pdf1_path)
pdf2_fonts = extract_fonts(pdf2_path)

# Compare fonts between the two PDFs
differences = compare_fonts(pdf1_fonts, pdf2_fonts)

# Show the differences
show_differences(differences)
