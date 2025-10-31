# Proyecto Aicor

Aplicación web de tienda online con Django en el backend y React en el frontend.  
Permite autenticación con Google, visualización de productos, gestión del carrito y simulación de compras.

---

## Instalación y ejecución del proyecto
**BACKEND**

**1 Crear y activar entorno virtual**
    cd backend
    python -m venv venv
    venv\Scripts\activate

**2 Instalar dependencias**
    pip install -r requirements.txt

**3 Aplicar migraciones**
    python manage.py migrate

**4 Ejecutar el servidor**
    python manage.py runserver

**FRONTEND**

**1 Instalar dependencias**
    cd frontend
    npm install

**2 Ejecutar el servidor de desarrollo**