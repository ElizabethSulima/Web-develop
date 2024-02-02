from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data
advertisements = []

# Create a new advertisement
@app.route('/advertisement', methods=['POST'])
def create_advertisement():
    data = request.get_json()
    title = data['title']
    description = data['description']
    owner = data['owner']
    
    # You can add validation here if required
    
    advertisement = {
        'title': title,
        'description': description,
        'owner': owner,
        'creation_date': str(datetime.now())
    }
    
    advertisements.append(advertisement)
    
    return jsonify({'message': 'Advertisement created successfully.'}), 201

# Get all advertisements
@app.route('/advertisements', methods=['GET'])
def get_advertisements():
    return jsonify(advertisements), 200

# Get a specific advertisement
@app.route('/advertisement/<int:advertisement_id>', methods=['GET'])
def get_advertisement(advertisement_id):
    advertisement = next((adv for adv in advertisements if adv['id'] == advertisement_id), None)
    
    if advertisement:
        return jsonify(advertisement), 200
    else:
        return jsonify({'message': 'Advertisement not found.'}), 404

# Delete an advertisement
@app.route('/advertisement/<int:advertisement_id>', methods=['DELETE'])
def delete_advertisement(advertisement_id):
    advertisement = next((adv for adv in advertisements if adv['id'] == advertisement_id), None)
    
    if advertisement:
        advertisements.remove(advertisement)
        return jsonify({'message': 'Advertisement deleted successfully.'}), 204
    else:
        return jsonify({'message': 'Advertisement not found.'}), 404

if __name__ == '__main__':
    app.run()
