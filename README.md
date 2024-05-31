# Proyecto de Reconocimiento de Imágenes con Detectron2

Este proyecto combina el uso de Detectron2 para la detección de objetos y una interfaz web desarrollada con React. Sigue los pasos a continuación para configurar y ejecutar el proyecto en tu entorno local.

## Prerrequisitos

- Python 3.8+
- Node.js 14+

## Instalación

### 1. Clonar el repositorio
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
### 2. Instalar dependencias de App.py
Primero, asegúrate de estar en el directorio del proyecto y luego instala las dependencias necesarias para App.py.

### 3. Instalar Detectron2
Para instalar Detectron2, ejecuta el siguiente comando:

pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu102/torch1.8/index.html

Asegúrate de cambiar la URL del archivo según tu versión de CUDA y PyTorch si es necesario.

### 4. Configurar y ejecutar la interfaz web
Navega al directorio Reto-WEB y levanta el proyecto con npm:

cd Reto-WEB

npm install

npm run dev

### 5. Ejecutar el script App.py
Regresa al directorio principal del proyecto y ejecuta App.py:

python App.py

Una vez que hayas completado los pasos anteriores, deberías tener el servidor backend y la interfaz web ejecutándose. Puedes acceder a la aplicación web en tu navegador web en http://localhost:3000.

