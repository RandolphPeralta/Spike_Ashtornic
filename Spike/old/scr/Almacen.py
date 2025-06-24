import os
import psycopg2
from pymongo import MongoClient

# Configuración para PostgreSQL
POSTGRES_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Yokona@76",
    "host": "localhost",
    "port": "5433"
}

# Configuración para MongoDB
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "extraccion_financiera"

def store_in_postgres(filename, text):
    """Almacena los datos en PostgreSQL."""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS datos_financieros (
                id SERIAL PRIMARY KEY,
                nombre_archivo TEXT,
                contenido TEXT
            )
        """)
        
        cursor.execute("INSERT INTO datos_financieros (nombre_archivo, contenido) VALUES (%s, %s)", (filename, text))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Datos de {filename} almacenados en PostgreSQL.")
    
    except Exception as e:
        print(f"Error al almacenar en PostgreSQL: {e}")

def store_in_mongodb(filename, text):
    """Almacena los datos en MongoDB."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db["datos_financieros"]
        
        collection.insert_one({"nombre_archivo": filename, "contenido": text})
        print(f"Datos de {filename} almacenados en MongoDB.")
    
    except Exception as e:
        print(f"Error al almacenar en MongoDB: {e}")

def process_structured_files(folder_path, storage_type="postgres"):
    """Procesa los archivos estructurados y los almacena en la base de datos seleccionada."""
    for filename in os.listdir(folder_path):
        if filename.endswith("_structured.txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            if storage_type == "postgres":
                store_in_postgres(filename, text)
            elif storage_type == "mongodb":
                store_in_mongodb(filename, text)
            else:
                print("Tipo de almacenamiento no soportado. Usa 'postgres' o 'mongodb'.")

if __name__ == "__main__":
    process_structured_files("C:/Users/Rando/OneDrive/Escritorio/Spike", storage_type="postgres")  # Cambia a 'mongodb' si prefieres MongoDB
