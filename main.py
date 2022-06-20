import requests
from flask import Flask, Response, jsonify
from flask_pydantic_spec import FlaskPydanticSpec
from pydantic import BaseModel
from tinydb import TinyDB, Query


server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Testando Flask')
spec.register(server)
db = TinyDB('database.json')


user = str(input('User: '))


r = requests.get(f'https://api.github.com/users/{user}/repos')
repos = r.json()

repo_list = list()

for repo in repos:
    repo_list.append(repo['name'])


db.insert({'name': user,'repositorios': repo_list})

class Repo_User(BaseModel):
    repo_user: list
    

@server.get('/repositorios')
def buscar_repositorios():
    """Mostra o Usuário e seus Repositórios no GitHub"""
    listas_repo = db.search(Query().name == user)
    return jsonify(
        Repo_User(
        repo_user = listas_repo  
        ).dict()
    )


server.run()




