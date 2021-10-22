from flask import Blueprint, request, jsonify
from werkzeug.wrappers import response
from homeworkAPI.helpers import token_required
from homeworkAPI.models import User, Coin, db, coin_schema, coins_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 38, 'another_value': 'Sockers FC'}

@api.route('/coins', methods=['POST'])
@token_required
def create_coin(current_user_token):
    name = request.json['name']
    max_supply = request.json['max_supply']
    utility = request.json['utility']
    token = current_user_token.token

    print(f'TEST: {current_user_token.token}')

    coin = Coin(name, utility, max_supply, user_token= token)
    
    db.session.add(coin)
    db.session.commit()

    response = coin_schema.dump(coin)
    return jsonify(response)

@api.route('/coins', methods = ['GET'])
@token_required
def get_coins(current_user_token):
    owner = current_user_token.token
    coins = Coin.query.filter_by(user_token = owner).all()
    response = coins_schema.dump(coins)
    return jsonify(response)

@api.route('/coins/<id>', methods = ['GET'])
@token_required
def get_coin(current_user_token, id):
    coin = Coin.query.get(id)
    response = coin_schema.dump(coin)
    return jsonify(response)

@api.route('/coins/<id>', methods = ['POST', 'PUT'])
@token_required
def update_coin(current_user_token, id):
    coin = Coin.query.get(id)
    print(coin)
    if coin:
        coin.name = request.json['name']
        coin.max_supply = request.json['max_supply']
        coin.utility = request.json['utility']
        coin.user_token = current_user_token.token
        db.session.commit()

        response = coin_schema(coin)
        return jsonify(response)
    else:
        return jsonify({'Error': "That coin does not exist."})

@api.route('/coins/<id>', methods = ['DELETE'])
@token_required
def delete_coin(current_user_token, id):
    coin = Coin.query.get(id)
    if coin:
        db.session.delete(coin)
        db.session.commit()
        return jsonify({'Success': f'Coin ID #{coin.id} has been deleted.'})
    else:
        jsonify({'Error': 'That coin does not exist.'})
