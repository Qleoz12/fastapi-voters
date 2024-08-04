# FastAPI demo portfolio project

This project is a FastAPI application
This project is a RESTful API that allows for efficient management and retrieval of data. It is built using Python and leverages several key technologies:

- **Poetry**: For dependency management and packaging.
- **SQLAlchemy**: For automatic database creation and ORM capabilities.
  
## Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- Poetry
- pycharm or vscode
  
## Setup

1. Install Poetry: https://python-poetry.org/docs/#installation
2. Install dependencies: `poetry install`
<!-- 3. Install pre-commit hooks: `poetry run pre-commit install` -->

## Running the app locally
using pycharm crun the main.py file or run the next command on the terminal
```bash
poetry run uvicorn main:app --reload
```

## Using the Postman Collection
A Postman collection is provided for testing the API. The collection contains requests for each endpoint in the API. The collection is located in the root directory of the project and is named api_gi_group.postman_collection.json.

Importing the Collection
1. Open Postman.
2. Click on Import in the upper left corner.
3. Select the File tab.
4. Click on Upload Files and choose the api_gi_group.postman_collection.json file located in the root directory of the project.
5. Click Import.

## docs 
check each ednpoint docs autogenerate by fastapi
http://localhost:8000/docs

## requirements

- [pending] Para obtener coordenadas, debe utilizarse el API de Georreferenciación de Google o similares.
- [done] Tener un servicio de Login (usuario y contraseña), que permita obtener un Token para
    consumir el resto de servicios.
    
    ```bash
    curl --location 'http://localhost:8000/sec/token' \
    --form 'username="admin@example.com"' \
    --form 'password="password123" 
    ```
    exist two users preload to db "admin@example.com" as ADMIN role and "notadmin@example.com", as LEAD role for testing purposes for both the password is "password123" 

- [done] El sistema deberá validar la existencia del Token en los servicios, para permitir acceder a la
 información. 
    
    each controller got rol validation bed on the token provided and the user role allows or denies access to the endpoint check the permisions on each endpoint somenthing like 
    ```python
    @authorize(role=[UserRole.ADMIN, UserRole.LEAD])
    ```
- [done] Cada servicio creado, debe tener un CRUD básico para gestionar la información.
 Exponer servicios que permitan realizar la gestión de Departamentos, Municipios, y mesas
 de votación.
    
    for each entity there is a controller with the basic CRUD operations, the next bath code show how consume each point get respectively 

    ```bash
    #Departamentos
    curl --location 'http://localhost:8000/states' \
    --header 'Authorization: Bearer {{token}}'
    
    #Municipios
    curl --location 'http://localhost:8000/municipalities' \
    --header 'Authorization: Bearer {{token}}
    
    #mesas de votación
    curl --location 'http://localhost:8000/votersTable' \
    --header 'Authorization: Bearer {{token}}'
    ```
  
- [done] Exponer un servicio que permita obtener la cantidad total de votantes inscritos por líder.
    
    The endpoint for retrieving voter information applies a filter based on the user's token. If the user is a leader, they can only view the data of voters they have created. However, if the user is an admin, they have access to view all voter data without restrictions.
    ```bash
    curl --location 'http://localhost:8000/voters' \
    --header 'Authorization: Bearer {{token}}'
    ```
- [done] Exponer un servicio que permita obtener la cantidad total de votantes, en el sistema. 
    
    the endpoin before resolve this problem to make the query with an admin user, but now the endpoint is open to all users

- [done] Exponer un servicio que permita obtener la cantidad total de votantes inscritos por
 municipio.

    consumes the next endpoint to get the total voters by municipality, remeber check the id code before consume the endpoint
    ```bash	
    curl --location 'http://localhost:8000/voters/municipality/1' \
    --header 'Authorization: Bearer {{token}}'
    ```
- [done] Exponer un servicio que permita obtener la cantidad total de votantes inscritos por mesa de
 votación.
     consumes the next endpoint to get the total voters by voterstable, remeber check the id code before consume the endpoint
    ```bash	
    curl --location 'http://localhost:8000/voters/votersTable/2' \
    --header 'Authorization: Bearer {{token}}'
    ```