from flask import Flask, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from bson.objectid import ObjectId
import os

# Carrega as variáveis de ambiente do arquivo .cred (se disponível)
load_dotenv('.cred')


app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)


# Este é um exemplo simples sem grandes tratamentos de dados
@app.route('/pacientes', methods=['GET'])
def get_all_users():

    filtro = {}
    projecao = {"_id" : 0}
    dados_pacientes = mongo.db.pacientes.find(filtro, projecao)

    resp = {
        "pacientes": list( dados_pacientes )
    }

    return resp, 200


# Este é um exemplo simples sem grandes tratamentos de dados
@app.route('/pacientes', methods=['POST'])
def post_user():
    
    data = request.json

    if "cpf" not in data:
        return {"erro": "cpf é obrigatório"}, 400
    
    # Certifique-se de que você está inserindo na coleção correta
    result = mongo.db.pacientes.insert_one(data)

    return {"id": str(result.inserted_id)}, 201



@app.route('/pacientes/<string:id>', methods=['GET'])
def get_one_user(id):
    try:
        # Tenta converter o 'id' recebido na URL para um ObjectId
        filtro = {"_id": ObjectId(id)}
    except:
        return {"erro": "ID inválido"}, 400

    # Faz a busca no MongoDB
    dados_paciente = mongo.db.pacientes.find_one(filtro, {"_id": 0})  # Projeta para excluir o campo _id da resposta

    if not dados_paciente:
        return {"erro": "Paciente não encontrado"}, 404

    return {"paciente": dados_paciente}, 200


# Rota para atualizar as informações de um paciente
@app.route('/pacientes/<string:id>', methods=['PUT'])
def update_user(id):
    try:
        filtro = {"_id": ObjectId(id)}
    except:
        return {"erro": "ID inválido"}, 400

    data = request.json

    # Atualiza o documento no MongoDB
    result = mongo.db.pacientes.update_one(filtro, {"$set": data})

    if not result:
        return {"erro": "Paciente não encontrado"}, 404

    return {"mensagem": "Paciente atualizado com sucesso"}, 200

# Rota para deletar um paciente
@app.route('/pacientes/<string:id>', methods=['DELETE'])
def delete_user(id):
    try:
        filtro = {"_id": ObjectId(id)}
    except:
        return {"erro": "ID inválido"}, 400

    result = mongo.db.pacientes.delete_one(filtro)

    if result.deleted_count == 0:
        return {"erro": "Paciente não encontrado"}, 404

    return {"mensagem": "Paciente deletado com sucesso"}, 200

if __name__ == '__main__':
    app.run(debug=True)