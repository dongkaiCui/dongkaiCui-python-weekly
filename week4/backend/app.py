from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/get', methods=['GET'])
def handle_get():
    params = request.args.get('params', '')
    return jsonify({'message': f'参数是 {params}'})

@app.route('/api/post', methods=['POST'])
def handle_post():
    data = request.get_json()
    body_params = data.get('body_params', '')
    param_params = request.args.get('param_params', '')
    return jsonify({
        'message': f'body中的参数是 {body_params}，param中的参数是 {param_params}'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)