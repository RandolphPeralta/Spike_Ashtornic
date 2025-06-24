import os
import json
import anthropic

def process_with_claude(text, document_type):
    """Procesa el texto con Claude 3 para estructurar la información financiera."""
    client = anthropic.Anthropic(api_key="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")
    
    # Prompt específico según el tipo de documento
    if document_type == "declaracion_renta":
        prompt = (
            "Extrae y estructura los siguientes datos financieros de una declaración de renta:\n"
            "1. Ingresos declarados: sueldos, honorarios, rentas, dividendos.\n"
            "2. Patrimonio bruto y neto: bienes inmuebles, inversiones, cuentas bancarias.\n"
            "3. Pasivos: deudas, créditos, hipotecas.\n"
            "4. Impuestos pagados y saldo a favor.\n"
            "Organiza la información en un formato JSON con las siguientes claves:\n"
            "- ingresos\n"
            "- patrimonio_bruto\n"
            "- patrimonio_neto\n"
            "- pasivos\n"
            "- impuestos_pagados\n"
            "- saldo_a_favor\n"
            f"Texto:\n{text}"
        )
    elif document_type == "informacion_exogena":
        prompt = (
            "Extrae y estructura los siguientes datos financieros de un reporte de información exógena:\n"
            "1. Ingresos reportados por terceros.\n"
            "2. Pagos de impuestos retenidos.\n"
            "3. Deducciones reportadas.\n"
            "Organiza la información en un formato JSON con las siguientes claves:\n"
            "- ingresos_reportados\n"
            "- impuestos_retenidos\n"
            "- deducciones\n"
            f"Texto:\n{text}"
        )
    elif document_type == "escrituras_publicas":
        prompt = (
            "Extrae y estructura los siguientes datos financieros de una escritura pública:\n"
            "1. Valor de compra o venta del inmueble.\n"
            "2. Fecha de transacción.\n"
            "3. Nombre de las partes involucradas.\n"
            "Organiza la información en un formato JSON con las siguientes claves:\n"
            "- valor_transaccion\n"
            "- fecha_transaccion\n"
            "- partes_involucradas\n"
            f"Texto:\n{text}"
        )
    elif document_type == "extractos_bancarios":
        prompt = (
            "Extrae y estructura los siguientes datos financieros de un extracto bancario o de tarjeta de crédito:\n"
            "1. Saldo inicial y final del periodo.\n"
            "2. Total de ingresos y egresos.\n"
            "3. Patrimonio líquido disponible.\n"
            "4. Deuda acumulada en tarjetas de crédito.\n"
            "Organiza la información en un formato JSON con las siguientes claves:\n"
            "- saldo_inicial\n"
            "- saldo_final\n"
            "- total_ingresos\n"
            "- total_egresos\n"
            "- patrimonio_liquido\n"
            "- deuda_tarjetas\n"
            f"Texto:\n{text}"
        )
    else:
        prompt = (
            "Extrae y estructura los datos financieros relevantes del siguiente texto. "
            "Organiza la información en un formato JSON con claves apropiadas.\n"
            f"Texto:\n{text}"
        )
    
    # Enviar la solicitud a Claude 3
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Convertir la respuesta en texto limpio
    structured_text = "\n".join([block.text for block in response.content])
    
    # Intentar convertir el texto en JSON
    try:
        structured_data = json.loads(structured_text)
    except json.JSONDecodeError:
        structured_data = {"error": "No se pudo estructurar la información en JSON."}
    
    return structured_data

def process_txt_files(input_folder, output_folder):
    """Procesa todos los archivos .txt en la carpeta con Claude 3."""
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            txt_path = os.path.join(input_folder, filename)
            print(f"Procesando con Claude 3: {filename}")
            
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            # Determinar el tipo de documento basado en el nombre del archivo
            if "declaracion_renta" in filename.lower():
                document_type = "declaracion_renta"
            elif "informacion_exogena" in filename.lower():
                document_type = "informacion_exogena"
            elif "escrituras_publicas" in filename.lower():
                document_type = "escrituras_publicas"
            elif "extractos_bancarios" in filename.lower():
                document_type = "extractos_bancarios"
            else:
                document_type = "otros"
            
            # Procesar el texto con Claude 3
            structured_data = process_with_claude(text, document_type)
            
            # Guardar los datos estructurados en un archivo JSON
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_structured.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(structured_data, f, indent=4, ensure_ascii=False)
            print(f"Datos estructurados guardados en {output_file}\n")

if __name__ == "__main__":
    # Rutas de las carpetas
    base_folder = "C:/Users/Rando/OneDrive/Escritorio/Spike - copia"
    input_folder = os.path.join(base_folder, "txt")
    output_folder = os.path.join(base_folder, "json")
    
    # Procesar los archivos .txt
    process_txt_files(input_folder, output_folder)