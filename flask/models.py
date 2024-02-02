from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advertisements.db'  # Подставьте свою строку подключения для базы данных
db = SQLAlchemy(app)

class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    owner = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'owner': self.owner
        }

db.create_all()

@app.route('/api/advertisements', methods=['POST'])
def create_advertisement():
    data = request.get_json()

    if 'title' not in data or 'description' not in data or 'owner' not in data:
        return jsonify({'error': 'Не указаны обязательные поля'}), 400

    advertisement = Advertisement(
        title=data['title'],
        description=data['description'],
        owner=data['owner']
    )

    db.session.add(advertisement)
    db.session.commit()

    return jsonify({'message': 'Объявление успешно создано'}), 201

@app.route('/api/advertisements/<int:id>', methods=['GET'])
def get_advertisement(id):
    advertisement = Advertisement.query.get(id)

    if not advertisement:
        return jsonify({'error': 'Объявление не найдено'}), 404

    return jsonify(advertisement.to_dict()), 200

@app.route('/api/advertisements/<int:id>', methods=['DELETE'])
def delete_advertisement(id):
    advertisement = Advertisement.query.get(id)

    if not advertisement:
        return jsonify({'error': 'Объявление не найдено'}), 404

    db.session.delete(advertisement)
    db.session.commit()

    return jsonify({'message': 'Объявление успешно удалено'}), 200

if __name__ == '__main__':
    app.run()