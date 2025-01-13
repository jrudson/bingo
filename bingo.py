import random
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import time

load_dotenv()
app = Flask(__name__)

CONNECTION_STRING = os.getenv("MONGO_URI")

client = MongoClient(CONNECTION_STRING)
db = client.get_database("my_database")
collection = db.get_collection("bingo_test")

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
    first_number = random_number()
    save = save_number(None, first_number)
    i = 1
    x = 0
    max_loop = 75
    # I need to change this logic to improve the code working
    # A idea is put all the numbers in an array and draw lots some, remove this and draw lot again without the number drawn
    while i < max_loop:
        print(f"i: {i}")
        data = list(collection.find({"_id": save}))
        this_id = data[0]['_id']
        next_number = random_number()
        while next_number in data[0]['tests']:
            x += 1
            next_number = random_number()
        save_number(this_id, next_number)
        i += 1
        time.sleep(2)
    data = list(collection.find({'_id': save}))
    new_data = data[0]['tests']
    sorted_data = sorted(new_data)
    return jsonify({'drawn_number': sorted_data}), 200

@app.route('/get_data', methods=['GET'])
def get_data():
    data = list(collection.find({}))
    for item in data:
        item['_id'] = str(item['_id'])
        print(item['_id'])
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(debug=True)
