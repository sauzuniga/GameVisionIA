 # GameVision IA 🎮



Aplicación web que predice el potencial comercial de un videojuego en Steam usando Machine Learning e inteligencia artificial generativa.



## Tecnologías



- **Backend:** FastAPI + SQLAlchemy + SQLite

- **Frontend:** React + Vite

- **Modelo:** Random Forest (scikit-learn)

- **Chatbot:** Gemini 1.5 Flash + LangChain

- **Base de datos:** SQLite



## Requisitos previos



- Python 3.11

- Node.js 18+

- Cuenta en [Google AI Studio](https://aistudio.google.com) para obtener una API key de Gemini



## Instalación



### 1. Clonar el repositorio


### 2. Agregar el modelo



El modelo `rf_model.pkl` no está incluido en el repositorio por su tamaño.  

Descargalo desde el siguiente enlace y colocalo en la carpeta `backend/`:



> (https://drive.google.com/file/d/13IYfQMRxx3-ZS70z5Hjs2ir8kre_j2_z/view?usp=sharing) ← 



### 3. Configurar el backend



```bash

py -3.11 -m venv venv

venv\Scripts\activate

cd backend

pip install -r requirements.txt

```



Creá el archivo `backend/.env` con tu API key de Gemini: GEMINI_API_KEY=tu_api_key_aqui
### 4. Configurar el frontend
```bash
cd frontend
npm install
```## Ejecución

Necesitás dos terminales abiertas:
**Terminal 1 — Backend:**
```bash
venv\Scripts\activate
cd backend
uvicorn main:app --reload
```
**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```
Luego abre el navegador en:- **Landing:** http://localhost:5173- **Aplicación:** http://localhost:5173/app- **API docs:** http://localhost:8000/docs
## Estructura del proyecto

## Seguridad


- La API key de Gemini se maneja exclusivamente en el backend mediante variables de entorno

- El archivo `.env` está excluido del repositorio

- CORS configurado para permitir solo el origen del frontend local



## Proyecto académico



Desarrollado como proyecto de graduación para la Pre-especialización en Desarrollo de Aplicaciones Inteligentes — Universidad Gerardo Barrios (UGB), 2026. 

¡