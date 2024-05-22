from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['library']
collection = db['books']

@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = list(collection.find())
    for book in books:
        book['_id'] = str(book['_id'])
    return jsonify(books), 200

@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = collection.find_one({'_id': ObjectId(id)})
    if book:
        book['_id'] = str(book['_id'])
        return jsonify(book), 200
    return jsonify({'error': 'Book not found'}), 404

@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    data = request.json
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Book updated'}), 200
    return jsonify({'error': 'Book not found'}), 404

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Book deleted'}), 200
    return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
