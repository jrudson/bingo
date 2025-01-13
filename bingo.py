import random
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
app = Flask(__name__)
print(f"The number is...")
print(f"Diretório atual: {os.getcwd()}")

CONNECTION_STRING = os.getenv("MONGO_URI")

print(f"CONNECTION_STRING: {CONNECTION_STRING}")

client = MongoClient(CONNECTION_STRING)
print("Conexão bem-sucedida")

db = client.get_database("my_database")
print(f"db: {db}")
collection = db.get_collection("bingo_test")
print(f"collection: {collection}")
data = {
    "name": "Jony",
    "team": "São Paulo"
}

collection.insert_one(data)

def random_number():
    drawn_number = random.randint(1, 75)
    return drawn_number

def save_number(id, number):
    if id is None:
        result = collection.insert_one({"tests": [number]})
        inserted_id = result.inserted_id
        return inserted_id
    else:
        find = {"_id": id}
        update = {"$push": {"tests": {"$each": [number]}}}
        collection.update_one(find, update)

# The route created always call the function below themself
@app.route('/random_number', methods=['GET'])

def number_generation():
    number = save_number()
    return jsonify({'drawn_number': number}), 200

if __name__ == '__main__':
    app.run(debug=True)
