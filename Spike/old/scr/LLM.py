import os
import json
import anthropic

def process_with_claude(text):
    """Procesa el texto con Claude 3 para estructurarlo."""
    client = anthropic.Anthropic(api_key="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")
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": f"Extrae y estructura los datos financieros del siguiente texto:\n{text}"}
        ]
    )
    
    # Convertir la respuesta en texto limpio
    structured_text = "\n".join([block.text for block in response.content])
    return structured_text

def process_txt_files(folder_path):
    """Procesa todos los archivos .txt en la carpeta con Claude 3."""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            txt_path = os.path.join(folder_path, filename)
            print(f"Procesando con Claude 3: {filename}")
            
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            structured_data = process_with_claude(text)
            
            output_file = f"{os.path.splitext(filename)[0]}_structured.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(structured_data)
            print(f"Datos estructurados guardados en {output_file}\n")

if __name__ == "__main__":
    process_txt_files("C:/Users/Rando/OneDrive/Escritorio/Spike")
