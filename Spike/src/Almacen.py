import os
import json
import psycopg2  # Para PostgreSQL

# Configuración de la base de datos PostgreSQL
POSTGRES_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "Yokona@76",
    "port": 5433
}

def connect_postgres():
    """Conectar a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        print("Conexión a PostgreSQL exitosa.")
        return conn
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None

def create_tables(conn):
    """Crear las tablas en PostgreSQL si no existen."""
    try:
        cursor = conn.cursor()
        
        # Tabla para Declaraciones de Renta
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS declaraciones_renta (
                id SERIAL PRIMARY KEY,
                año INTEGER,
                ingresos JSONB,
                patrimonio_bruto JSONB,
                patrimonio_neto FLOAT,
                pasivos JSONB,
                impuestos_pagados FLOAT,
                saldo_a_favor FLOAT
            )
        """)
        
        # Tabla para Información Exógena
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS informacion_exogena (
                id SERIAL PRIMARY KEY,
                año INTEGER,
                ingresos_reportados JSONB,
                impuestos_retenidos FLOAT,
                deducciones JSONB
            )
        """)
        
        # Tabla para Escrituras Públicas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS escrituras_publicas (
                id SERIAL PRIMARY KEY,
                valor_transaccion FLOAT,
                fecha_transaccion DATE,
                partes_involucradas JSONB
            )
        """)
        
        # Tabla para Extractos Bancarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS extractos_bancarios (
                id SERIAL PRIMARY KEY,
                saldo_inicial FLOAT,
                saldo_final FLOAT,
                total_ingresos FLOAT,
                total_egresos FLOAT,
                patrimonio_liquido FLOAT,
                deuda_tarjetas FLOAT
            )
        """)
        
        # Tabla para Otros Documentos Financieros
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS otros_documentos (
                id SERIAL PRIMARY KEY,
                tipo_documento TEXT,
                datos JSONB
            )
        """)
        
        conn.commit()
        print("Tablas creadas o verificadas en PostgreSQL.")
    except Exception as e:
        print(f"Error al crear tablas en PostgreSQL: {e}")

def insert_into_postgres(conn, data, document_type):
    """Insertar datos en PostgreSQL según el tipo de documento."""
    try:
        cursor = conn.cursor()
        
        if document_type == "declaracion_renta":
            cursor.execute("""
                INSERT INTO declaraciones_renta (año, ingresos, patrimonio_bruto, patrimonio_neto, pasivos, impuestos_pagados, saldo_a_favor)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                data.get("año"),
                json.dumps(data.get("ingresos", {})),
                json.dumps(data.get("patrimonio_bruto", {})),
                data.get("patrimonio_neto", 0.0),
                json.dumps(data.get("pasivos", {})),
                data.get("impuestos_pagados", 0.0),
                data.get("saldo_a_favor", 0.0)
            ))
        
        elif document_type == "informacion_exogena":
            cursor.execute("""
                INSERT INTO informacion_exogena (año, ingresos_reportados, impuestos_retenidos, deducciones)
                VALUES (%s, %s, %s, %s)
            """, (
                data.get("año"),
                json.dumps(data.get("ingresos_reportados", {})),
                data.get("impuestos_retenidos", 0.0),
                json.dumps(data.get("deducciones", {}))
            ))
        
        elif document_type == "escrituras_publicas":
            cursor.execute("""
                INSERT INTO escrituras_publicas (valor_transaccion, fecha_transaccion, partes_involucradas)
                VALUES (%s, %s, %s)
            """, (
                data.get("valor_transaccion", 0.0),
                data.get("fecha_transaccion"),
                json.dumps(data.get("partes_involucradas", {}))
            ))
        
        elif document_type == "extractos_bancarios":
            cursor.execute("""
                INSERT INTO extractos_bancarios (saldo_inicial, saldo_final, total_ingresos, total_egresos, patrimonio_liquido, deuda_tarjetas)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                data.get("saldo_inicial", 0.0),
                data.get("saldo_final", 0.0),
                data.get("total_ingresos", 0.0),
                data.get("total_egresos", 0.0),
                data.get("patrimonio_liquido", 0.0),
                data.get("deuda_tarjetas", 0.0)
            ))
        
        elif document_type == "otros":
            cursor.execute("""
                INSERT INTO otros_documentos (tipo_documento, datos)
                VALUES (%s, %s)
            """, (
                "otros",
                json.dumps(data)
            ))
        
        conn.commit()
        print(f"Datos insertados en PostgreSQL para el tipo de documento: {document_type}")
    except Exception as e:
        print(f"Error al insertar en PostgreSQL: {e}")

def process_json_files(folder_path):
    """Procesar todos los archivos JSON en la carpeta y almacenarlos en PostgreSQL."""
    conn = connect_postgres()
    if not conn:
        return
    
    # Crear las tablas si no existen
    create_tables(conn)
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            json_path = os.path.join(folder_path, filename)
            print(f"Procesando: {filename}")
            
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
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
            
            # Insertar los datos en PostgreSQL
            insert_into_postgres(conn, data, document_type)
    
    # Cerrar la conexión
    conn.close()

if __name__ == "__main__":
    # Especificar la carpeta con los archivos JSON
    folder_path = "C:/Users/Rando/OneDrive/Escritorio/Spike - copia/json"
    process_json_files(folder_path)