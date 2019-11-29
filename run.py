from flask import Flask, render_template, request
import json
from query_processor import answer

app = Flask(__name__)

@app.route('/', methods=['POST'])
def post():
	query = request.json


	return json.dumps(answer(query), ensure_ascii=False, indent=4)



app.run(host='0.0.0.0', port=3389)


