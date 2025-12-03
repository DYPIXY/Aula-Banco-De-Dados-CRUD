from flask import Flask, jsonify, request
import mysql.connector
import json 
import random
import string
import hashlib

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="localhost",
  user="usuario",
  password="aula",
  database='aula_m3'
)

mysqlIt = mydb.cursor(buffered=True)

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
        id = str(content['id'])
        nome = str(content['nome'])
        email = str(content['email'])

        #calc do sha256 da senha
        passwordRaw = str(content['senha'])        
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=12)) #gera strings com tamanho de 12 caracteres aleatórios

        sha = hashlib.sha256()
        sha.update(passwordRaw.encode('ascii') + salt.encode('ascii'))
        password = sha.hexdigest()

        mysqlIt.execute("UPDATE passwords " \
                        "SET password = %s" \
                        "   ,salt = %s" \
                        "WHERE user_id = %s", (password, salt, id))
        mysqlIt.execute("UPDATE user " \
                        "SET nome = %s" \
                        "   ,email = %s" \
                        "WHERE id = %s", (nome, email, id))
        mydb.commit()
    except Exception as e:
        print(e)
        return {'message': "Erro ao atualizar usuário", 'erro': str(e)}, 400
    
    return {'message': 'Usuário alterado com sucesso'}, 200

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
        result = mysqlIt.fetchone()
        user = { 
                'id': result[0],
                'nome': result[1],
                'email': result[2],
                'created_at': result[3].isoformat() if result[3] is not None else '',
                'updated_at': result[4].isoformat() if result[4] is not None else '',
                'deleted_at': result[5].isoformat() if result[5] is not None else '',
            }
    except Exception as e:
        print(e)
        return {'message': "Erro ao buscar usuário", 'erro': str(e)}, 400
    
    return {'message': 'Sucesso ao buscar no banco', 'user': user}, 200


#notes
@app.route('/notes/create', methods=['POST'])
def notesCreate():
    content = request.json

    try:
        mysqlIt.execute("INSERT INTO notes(texto, user_id, tipo_id) VALUES (%s, %s, %s)", (content['texto'], content['user_id'], content['tipo_id']))
        mydb.commit()
    except Exception as e:
        print(e)
        return {'message': "Erro ao criar nota", 'erro': str(e)}, 400
    
    return {'message': 'Nota criada com sucesso'}, 200

@app.route('/notes/update', methods=['POST'])
def notesUpdate():
    content = request.json

    try:
        id = str(content['id'])
        texto = str(content['texto'])
        tipo = str(content['tipo_id'])

        mysqlIt.execute("UPDATE notes " \
                        "SET texto = %s" \
                        "   ,tipo_id = %s" \
                        "WHERE id = %s", (texto, tipo, id))
        mydb.commit()
    except Exception as e:
        print(e)
        return {'message': "Erro ao atualizar nota", 'erro': str(e)}, 400
    
    return {'message': 'Nota alterada com sucesso'}, 200

@app.route('/notes/retrieve', methods=['GET'])
def notesRetrieve():
    content = request.json

    notes = ""
    try:
        id = str(content['user_id']),
        mysqlIt.execute("SELECT " \
                        "    n.id, " \
                        "    n.texto, " \
                        "    nt.tipo, " \
                        "    nt.definitions " \
                        " FROM notes n " \
                        " INNER JOIN note_type nt " \
                        "    on nt.id = n.tipo_id" \
                        " where n.user_id = %s", id)
        if not mysqlIt.rowcount:
            raise Exception("Notas não encontradas")
        
        # transforma em json e devolve o resultado
        result = mysqlIt.fetchall()
        
        notes = [{ 
            'id': i[0],
            'texto': i[1],
            'tipo': i[2],
            'definitions': i[3],
        }
        for i in result]

    except Exception as e:
        print(e)
        return {'message': "Erro ao buscar notas", 'erro': str(e)}, 400
    
    return {'message': 'Sucesso ao buscar no banco', 'user': notes}, 200


@app.route('/notes/delete', methods=['POST'])
def notesDelete():
    content = request.json

    try:
        id = str(content['id']),
        mysqlIt.execute("DELETE FROM notes WHERE id = %s", id)
        mydb.commit()
    except Exception as e:
        print(e)
        return {'message': "Erro ao deletar nota", 'erro': str(e)}, 400
    
    return {'message': 'Nota deletada com sucesso'}, 200


#error handling
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'Route not found'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'message': 'Method not allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True)
