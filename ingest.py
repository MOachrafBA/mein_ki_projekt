from pypdf import PdfReader

pdf_file = "Bacheloarbeit_Mohamed_Achraf_Badaoui_638071.pdf"
#reader = PdfReader(pdf_file)
#number_of_pages = len(reader.pages)
#page = reader.pages[0]
#text = page.extract_text()
#print(number_of_pages)
#print(text)

def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

if __name__ == "__main__":
    pdf_text = load_pdf(pdf_file)
    print(f"Vorschau des extrahierte Textes:\n{pdf_text[:10000]}")  # Zeigt die ersten X Zeichen des extrahierten Textes an