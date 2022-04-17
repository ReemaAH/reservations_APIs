FROM reemaah/custom-python:3.10.4-slim-buster

# 1. create working directory
RUN mkdir /code
WORKDIR /code 

#2. copy all code files
COPY . /code/

#3 change working dorectory to django project
WORKDIR /code/resturant_API

# 4. create virtual env
RUN python3 -m venv env

# 5. Install dependencies
RUN ./env/bin/pip install -r requirements.txt

# 6. copy docker-entrypoint.sh to local folder
COPY ./docker-entrypoint.sh .

# 7. run docker-entrypoint
RUN ["chmod", "+x", "./docker-entrypoint.sh"]

