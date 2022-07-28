from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/api/players', methods=['GET'])
def players():

    if request.method == 'GET':
        df = pd.read_csv('./static/js/Searchable_Players_2022.csv')
        return {'players': df.to_dict()}, 200

if __name__ == '__main__':
    app.run(debug=True)