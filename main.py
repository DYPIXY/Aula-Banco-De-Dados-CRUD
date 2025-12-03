from flask import Flask, jsonify, request
import mysql.connector
import json 

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="localhost",
  user="usuario",
  password="aula",
  database='aula_m3'
)

mysqlIt = mydb.cursor()

#user
@app.route('/user/create', methods=['POST'])
def userCreate():
    content = request.json

    id = None
    try:
        mysqlIt.execute("INSERT INTO user(nome, email) VALUES (%s, %s)", (content['nome'], content['email']))
        mysqlIt.execute("SELECT id FROM user WHERE email = %s and nome = %s", (content['email'], content['nome']))
        id = mysqlIt.fetchone()
        mydb.commit()
    except Exception as e:
        print(e)
        return {'message': "Erro ao criar usuário", 'erro': str(e)}, 400
    
    return {'message': 'Usuário criado com sucesso','id': id}, 200

@app.route('/user/delete', methods=['POST'])
def userDelete():
    content = request.json

    try:
        id = str(content['id']),
        mysqlIt.execute("DELETE FROM user WHERE id = %s", id)
        mydb.commit()
    except Exception as e:
        print(e)
        return {'message': "Erro ao deletar usuário", 'erro': str(e)}, 400
    
    return {'message': 'Usuário deletado com sucesso'}, 200

@app.route('/user/update', methods=['POST'])
def userUpdate():
    content = request.json

    try:
        id = str(content['id']),
        mysqlIt.execute("DELETE FROM user WHERE id = %s", id)
        mydb.commit()
    except Exception as e:
        print(e)
        return {'message': "Erro ao deletar usuário", 'erro': str(e)}, 400
    
    return {'message': 'Usuário deletado com sucesso'}, 200

@app.route('/user/retrieve', methods=['GET'])
def userRetrieve():
    content = request.json

    user = ""
    try:
        id = str(content['id']),
        mysqlIt.execute("SELECT * FROM user where id = %s", id)
        if not mysqlIt.rowcount:
            raise Exception("Usuário não encontrado")
        
        # transforma em json e devolve o resultado
        row_headers=[x[0] for x in mysqlIt.description]
        rv = mysqlIt.fetchall()
        json_data=[]
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        return {'message': 'Sucesso ao buscar no banco', 'user': json.dumps(json_data)}, 200
    except Exception as e:
        print(e)
        return {'message': "Erro ao deletar usuário", 'erro': str(e)}, 400
    
    return {'message': 'Sucesso ao buscar no banco', 'user': user}, 200


#notes
@app.route('/notes/create', methods=['POST'])
def notesCreate():
    return {'message': 'Welcome to My API'}, 200

@app.route('/notes/update', methods=['POST'])
def notesUpdate():
    return {'message': 'Welcome to My API'}, 200

@app.route('/notes/retrieve', methods=['GET'])
def notesRetrieve():
    return {'message': 'Welcome to My API'}, 200

@app.route('/notes/delete', methods=['POST'])
def notesDelete():
    return {'message': 'Welcome to My API'}, 200


#error handling
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'Route not found'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'message': 'Method not allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True)
