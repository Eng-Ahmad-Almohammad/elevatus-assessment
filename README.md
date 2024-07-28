# Elevatus assessment

This is a simple FastApi for managing Candidate Profiles. Basically, we will have two collections, user
and candidate. The user can create, view, delete and update candidate profiles. The user should be
able to search for specific candidates.

```
Foe API document make sure to hit the '/docs' or '/redoc' endpoint.
```

## Running the app

### Run using Docker

- Download Docker from the following [link](https://www.docker.com/products/docker-desktop/) and docker-compose using the following command

```bash
sudo pip install docker-compose
```

- Create .env file on the top level of the directories tree and fill it as the .env.sample but do not change the value of the `MONGODB_HOST` and `MONGODB_PORT`.

- After creating the .env file all what you need to do is to run:

```bash
docker-compose up --build
```

### Run using Terminal

- You must have python 3.10+

- Create virtual environment by running the following command

```bash
pip install requirements/development.txt
```

- Create an account on [Mongo Atlas](https://www.mongodb.com/products/platform/atlas-database) and follow the steps to create you first cluster and database.

- Create .env file on the top level of the directories tree and fill it as the .env.sample

- Run the following command to run the server

```bash
uvicorn main:create_app --reload --port 8000
```
