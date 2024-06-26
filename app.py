from flask import Flask, jsonify, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models.user import User
from database import db
import bcrypt


app = Flask(__name__)
app.config.from_pyfile('settings.py')
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


def hash_password(password):
    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    return hashed_password.decode()

def check_password(password, user_password):
    return bcrypt.checkpw(str.encode(password), str.encode(user_password))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and check_password(password, user.password):
            login_user(user)
            return jsonify({"message": "Autenticação realizada com sucesso"})
    return jsonify({"message": "Credenciais inválidas"}), 400


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"})


@app.route('/user', methods=['POST'])
# @login_required
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, password=hash_password(password), role='user')
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "Usuário cadastrado com sucesso"})

    return jsonify({"message": "Dados inválidos"}), 401


@app.route('/user/<uuid:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)
    if user:
        return {
            "id": user.id,
            "username": user.username
            }
    return jsonify({"message": "Usuário não encontrado"}), 404


@app.route('/user/<uuid:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == 'user':
        return jsonify({"message": "Operação não permitida"}), 403
    if user and data.get('password'):
        user.password = hash_password(data.get('password'))
        db.session.commit()
        return jsonify(
            {"message": f"Usuário {id_user} atualizado com sucesso"}
            )
    return jsonify({"message": "Usuário não encontrado"}), 404


@app.route('/user/<uuid:id_user>', methods=['DELETE'])
@login_required
def delete(id_user):
    user = User.query.get(id_user)
    if user:
        if current_user.role != 'admin':
            return jsonify({"message": "Operação não permitida"}), 403
        if id_user == current_user.id:
            return jsonify(
                {"message": "Não é possível deletar o usuário conectado"}
                ), 403
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} deletado com sucesso"})
    return jsonify({"message": "Usuário não encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True)
