# 🎯 Ensamble API

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![ML](https://img.shields.io/badge/ML-RandomForest-green?style=for-the-badge&logo=scikit-learn)

API REST para predicciones con modelos de Machine Learning basados en ensambles de *RandomForest from Scratch*
</div>

[Características](#-características) •
[Instalación](#-instalación) •
[Uso](#-uso) •
[API Docs](#-documentación-de-la-api) •


---

## 📋 Descripción

**Ensamble API** es una API REST construida con FastAPI que despliega un modelo de predicción basado en RandomForest. Proporciona endpoints para realizar predicciones, monitoreo de salud y obtener información sobre la configuración del modelo.

## ✨ Características

- 🚀 **Alta Performance**: Construida con FastAPI para máxima velocidad
- 🔮 **Predicciones ML**: Modelo de ensamble RandomForest optimizado
- 📊 **Monitoreo**: Endpoints de health check y métricas
- 📚 **Documentación Automática**: Swagger UI y ReDoc incluidos
- 🛡️ **Manejo de Errores**: Respuestas consistentes y descriptivas
- ⚡ **Async Ready**: Soporte para operaciones asíncronas

## 🛠️ Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/marti/ensamble-api.git
cd ensamble-api
```

2. **Crear entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install -r ./app/requirements.txt
```

4. **Ejecutar la aplicación**
```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

## 🚀 Uso

### Endpoints Principales

#### Health Check
```bash
GET /health
```
Verifica el estado de la API

#### Información del Modelo
```bash
GET /info
```
Obtiene metadata y configuración del modelo

#### Predicciones
```bash
POST /predict
Content-Type: application/json

{
  "features": [1.5, 2.3, 4.5, ...]
}
```

### Ejemplo con Python

```python
import requests

# Realizar predicción
response = requests.post(
    "http://localhost:8000/predict",
    json={"features": [1.5, 2.3, 4.5, 3.2]}
)

prediction = response.json()
print(f"Predicción: {prediction}")
```

## 📚 Documentación de la API

Una vez que la aplicación esté corriendo, accede a la documentación interactiva:

- **Swagger UI**: http://localhost:8000/docs

## 📁 Estructura del Proyecto

```
ensamble-api/
├── app/
│   ├── requirements.txt     # Dependencias
│   ├── main.py              # Aplicación principal
│   ├── routers/             # Endpoints organizados
│   │   ├── health.py        # Health checks
│   │   ├── info.py          # Información del modelo
│   │   └── predict.py       # Predicciones
└── README.md
```

## 🔧 Configuración

Puedes configurar la aplicación mediante variables de entorno:

```bash
# .env
API_BASE_URL=http://localhost:8000
```


## 📊 Tecnologías

- **Framework**: FastAPI
- **ML**: Scikit-learn (DecissionTree)
- **Servidor**: Uvicorn
- **Validación**: Pydantic

<div align="center">
Hecho con ❤️ y ☕
</div>