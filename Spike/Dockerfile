# Usa una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de la aplicación (ajústalo si es diferente)
EXPOSE 8000

# Comando para ejecutar la aplicación (ajustar según el framework)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
