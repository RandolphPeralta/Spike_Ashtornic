import os
import PyPDF2
import pdfplumber

def extract_text_pypdf2(pdf_path):
    """Extrae texto de un PDF estructurado usando PyPDF2."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_pdfplumber(pdf_path):
    """Extrae texto de un PDF estructurado usando pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def process_pdfs(folder_path):
    """Procesa todos los PDFs en la carpeta y extrae su contenido."""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Procesando: {filename}")
            
            text_pypdf2 = extract_text_pypdf2(pdf_path)
            text_pdfplumber = extract_text_pdfplumber(pdf_path)
            
            extracted_text = text_pypdf2 if text_pypdf2.strip() else text_pdfplumber
            
            output_file = f"{os.path.splitext(filename)[0]}.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"Texto extraído guardado en {output_file}\n")

if __name__ == "__main__":
    process_pdfs("C:/Users/Rando/OneDrive/Escritorio/Spike")