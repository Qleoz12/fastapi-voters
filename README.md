# FastAPI demo portfolio project

This project is a FastAPI application designed to connect to AWS Bedrock

## Setup

1. Install Poetry: https://python-poetry.org/docs/#installation
2. Install dependencies: `poetry install`
3. Install pre-commit hooks: `poetry run pre-commit install`

## Running the app locally

```bash
poetry run uvicorn main:app --reload
```

## docs 
http://localhost:8000/docs

## requirements

- [pending] Para obtener coordenadas, debe utilizarse el API de Georreferenciación de Google o similares.
- done Tener un servicio de Login (usuario y contraseña), que permita obtener un Token para
 consumir el resto de servicios.
-[done] El sistema deberá validar la existencia del Token en los servicios, para permitir acceder a la
 información. 
-[done] Cada servicio creado, debe tener un CRUD básico para gestionar la información.
 Exponer servicios que permitan realizar la gestión de Departamentos, Municipios, y mesas
 de votación.
  
- Exponer un servicio que permita obtener la cantidad total de votantes inscritos por líder.
- Exponer un servicio que permita obtener la cantidad total de votantes, en el sistema. 
- Exponer un servicio que permita obtener la cantidad total de votantes inscritos por
 municipio.
- Exponer un servicio que permita obtener la cantidad total de votantes inscritos por mesa de
 votación.