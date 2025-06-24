import os
import PyPDF2
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

# Configuración de Tesseract OCR (ruta al ejecutable de Tesseract)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_pypdf2(pdf_path):
    """Extrae texto de un PDF estructurado usando PyPDF2."""
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error al extraer texto con PyPDF2: {e}")
    return text

def extract_text_pdfplumber(pdf_path):
    """Extrae texto de un PDF estructurado usando pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error al extraer texto con pdfplumber: {e}")
    return text

def extract_text_ocr_tesseract(pdf_path):
    """Extrae texto de un PDF escaneado usando Tesseract OCR."""
    text = ""
    try:
        # Convertir PDF a imágenes
        images = convert_from_path(pdf_path)
        for image in images:
            text += pytesseract.image_to_string(image, lang='spa') + "\n"  # 'spa' para español
    except Exception as e:
        print(f"Error al extraer texto con Tesseract OCR: {e}")
    return text

def process_pdfs(input_folder, output_folder):
    """Procesa todos los PDFs en la carpeta y extrae su contenido."""
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            print(f"Procesando: {filename}")
            
            # Intentar extraer texto de PDFs estructurados
            text_pypdf2 = extract_text_pypdf2(pdf_path)
            text_pdfplumber = extract_text_pdfplumber(pdf_path)
            
            # Si no se extrae texto, asumir que es un PDF escaneado y usar OCR
            if text_pypdf2.strip() or text_pdfplumber.strip():
                extracted_text = text_pypdf2 if text_pypdf2.strip() else text_pdfplumber
            else:
                print("El PDF parece estar escaneado. Aplicando OCR...")
                extracted_text = extract_text_ocr_tesseract(pdf_path)
            
            # Guardar el texto extraído en un archivo .txt
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"Texto extraído guardado en {output_file}\n")

if __name__ == "__main__":
    # Rutas de las carpetas
    base_folder = "C:/Users/Rando/OneDrive/Escritorio/Spike - copia"
    input_folder = os.path.join(base_folder, "pdf")
    output_folder = os.path.join(base_folder, "txt")
    
    # Procesar los PDFs
    process_pdfs(input_folder, output_folder)