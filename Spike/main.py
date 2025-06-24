import subprocess
import os
import time

# Rutas de los scripts
SCRIPTS_FOLDER = "src"
EXTRACTION_SCRIPT = os.path.join(SCRIPTS_FOLDER, "Extracion.py")
LLM_SCRIPT = os.path.join(SCRIPTS_FOLDER, "LLM.py")
ALMACEN_SCRIPT = os.path.join(SCRIPTS_FOLDER, "Almacen.py")
VISUALIZACION_SCRIPT = os.path.join(SCRIPTS_FOLDER, "Visualizacion.py")

def run_script(script_path):
    """Ejecuta un script Python y maneja errores."""
    try:
        print(f"Ejecutando: {script_path}")
        result = subprocess.run(["python", script_path], check=True)
        if result.returncode == 0:
            print(f"{script_path} se ejecutó correctamente.")
        else:
            print(f"Error al ejecutar {script_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Error en {script_path}: {e}")
    except FileNotFoundError:
        print(f"El archivo {script_path} no existe.")
    except Exception as e:
        print(f"Error inesperado en {script_path}: {e}")

def main():
    print("Iniciando el proceso de extracción, procesamiento y visualización de datos...")

    # Paso 1: Ejecutar Extracion.py
    run_script(EXTRACTION_SCRIPT)
    print("Esperando a que se complete la extracción de datos...")
    time.sleep(2)  # Pequeña pausa para asegurar que los archivos .txt se generen

    # Verificar si la carpeta "txt" tiene archivos
    txt_folder = "txt"
    if not os.path.exists(txt_folder) or not os.listdir(txt_folder):
        print("Error: No se encontraron archivos .txt en la carpeta 'txt'.")
        return

    # Paso 2: Ejecutar LLM.py
    run_script(LLM_SCRIPT)
    print("Esperando a que se complete el procesamiento con LLM...")
    time.sleep(2)  # Pequeña pausa para asegurar que los archivos .json se generen

    # Verificar si la carpeta "json" tiene archivos
    json_folder = "json"
    if not os.path.exists(json_folder) or not os.listdir(json_folder):
        print("Error: No se encontraron archivos .json en la carpeta 'json'.")
        return

    # Paso 3: Ejecutar Almacen.py
    run_script(ALMACEN_SCRIPT)
    print("Esperando a que se complete el almacenamiento en PostgreSQL...")
    time.sleep(2)  # Pequeña pausa para asegurar que los datos se inserten en la base de datos

    # Paso 4: Ejecutar Visualizacion.py
    print("Iniciando el dashboard de visualización...")
    run_script(VISUALIZACION_SCRIPT)

    print("Proceso completado.")

if __name__ == "__main__":
    main()