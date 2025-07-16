from flask import Flask, request, jsonify, render_template
from datetime import datetime
from extensions import db        
from models import URL           
from utils import generate_short_code

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# Homepage: Show the frontend page
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint: Create a short URL
@app.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Generate unique short code
    short_code = generate_short_code()
    while URL.query.filter_by(shortCode=short_code).first():
        short_code = generate_short_code()

    # Create and save new record
    new_url = URL(
        url=url,
        shortCode=short_code,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )

    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        "id": new_url.id,
        "url": new_url.url,
        "shortCode": new_url.shortCode,
        "createdAt": new_url.createdAt.isoformat(),
        "updatedAt": new_url.updatedAt.isoformat()
    }), 201

# GET /shorten/<shortCode> - Retrieve original URL
@app.route('/shorten/<shortCode>', methods=['GET'])
def get_original_url(shortCode):
    url_entry = URL.query.filter_by(shortCode=shortCode).first()
    if url_entry:
        url_entry.accessCount += 1  # track usage
        url_entry.updatedAt = datetime.utcnow()
        db.session.commit()
        return jsonify({
            "id": url_entry.id,
            "url": url_entry.url,
            "shortCode": url_entry.shortCode,
            "createdAt": url_entry.createdAt.isoformat(),
            "updatedAt": url_entry.updatedAt.isoformat()
        }), 200
    return jsonify({"error": "Short URL not found"}), 404


# PUT /shorten/<shortCode> - Update original URL
@app.route('/shorten/<shortCode>', methods=['PUT'])
def update_url(shortCode):
    url_entry = URL.query.filter_by(shortCode=shortCode).first()
    if not url_entry:
        return jsonify({"error": "Short URL not found"}), 404

    data = request.get_json()
    new_url = data.get('url')
    if not new_url:
        return jsonify({"error": "New URL is required"}), 400

    url_entry.url = new_url
    url_entry.updatedAt = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "id": url_entry.id,
        "url": url_entry.url,
        "shortCode": url_entry.shortCode,
        "createdAt": url_entry.createdAt.isoformat(),
        "updatedAt": url_entry.updatedAt.isoformat()
    }), 200


# DELETE /shorten/<shortCode> - Delete short URL
@app.route('/shorten/<shortCode>', methods=['DELETE'])
def delete_url(shortCode):
    url_entry = URL.query.filter_by(shortCode=shortCode).first()
    if not url_entry:
        return jsonify({"error": "Short URL not found"}), 404

    db.session.delete(url_entry)
    db.session.commit()
    return '', 204  # No Content


# GET /shorten/<shortCode>/stats - Get stats
@app.route('/shorten/<shortCode>/stats', methods=['GET'])
def get_url_stats(shortCode):
    url_entry = URL.query.filter_by(shortCode=shortCode).first()
    if not url_entry:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({
        "id": url_entry.id,
        "url": url_entry.url,
        "shortCode": url_entry.shortCode,
        "createdAt": url_entry.createdAt.isoformat(),
        "updatedAt": url_entry.updatedAt.isoformat(),
        "accessCount": url_entry.accessCount
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
