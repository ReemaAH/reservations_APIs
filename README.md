# Resturnat reservations Project

## Motivation
The idea of this project is to create a backend system that enables the restaurant workers to easily reserve tables based on the size of customer's groups.


## Getting Started
### URLs
- Locally: http://127.0.0.1:8000/

### Postman collection link:
https://go.postman.co/workspace/My-Workspace~e85051d8-fb36-4eee-8252-8d3d692f6f35/collection/13494285-abbe333a-a606-41ef-babb-8e01f89a08f2?action=share&creator=13494285


### To running the server locally you can do either a or b:

### a) by running services in docker-compose
- make sure you installed docker or visit this link: https://docs.docker.com/get-docker/
- make sure you installed docker-compose: https://docs.docker.com/compose/install/ 
- run the following command to run docker-compose 
``` docker-compose up -d ```

### b) by installing dependencies 

#### 1. Installing Python
#Python 3.10.4
Follow instructions to install the latest version of python here (https://docs.python.org/3/)


#### 2. Creating a virtual enviornment
Run the following command to create virtual Enviornment and activate it:
 ``` python3 -m venv env  ```
 ```source env/bin/activate  ```


#### 3. CD to resturant_API folder
This is the Django project folder.


#### 4. Installing project dependencies by pip
Install dependencies by running:
```pip install -r requirements.txt```
This will install all of the required packages within the requirements.txt file.


#### 5. Setup a Postgresql DB server
you can do it by running a docker container:
``` docker run --name postgresq -e POSTGRES_USER=admin_user -e POSTGRES_PASSWORD=passw0rd  -e POSTGRES_DB=resturant -d -p 5432:5432 -v postgres_resturant:/var/lib/postgresql/data postgres:9.6.12 ```


#### 6. Setup a Redis server
you can do it by running a docker container:
``` docker run --name redis -p 6379:6379 -d redis ```


#### 7. Migrate to DB
Run the following command to migrate db migrations:
``` python manage.py migrate``` 


#### 8. Run dump_db
Run the following command to dump db with admin group:
``` python manage.py db_dump``` 


#### 9. Create a super user
Run the following command to create a super user:
``` python manage.py createsuperuser``` 


#### 10. Run the server
Run the following command to run the server:
``` python manage.py runserver``` 



#### 11. to run integration test
Please run the following commands:

``` coverage run manage.py test``` 
``` coverage report ``` 
``` coverage html ``` 


