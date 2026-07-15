from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from db_helper import MySQLHelper

app = Flask(__name__)
CORS(app)

@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    db = MySQLHelper(database="spider_db")
    data = db.execute("SELECT title, rating FROM douban_top100 ORDER BY rating DESC LIMIT 20")
    db.close()
    return jsonify({
        'titles': [row[0] for row in data],
        'ratings': [row[1] for row in data]
    })

@app.route('/api/years', methods=['GET'])
def get_years():
    db = MySQLHelper(database="spider_db")
    data = db.execute("SELECT year, COUNT(*) FROM douban_top100 WHERE year > 0 GROUP BY year")
    db.close()
    return jsonify({
        'years': [row[0] for row in data],
        'counts': [row[1] for row in data]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)