from flask import Flask, render_template, request
import json

app = Flask(__name__)



@app.route('/', methods=['POST'])
def post():
	print(request.json)
	resp = {
		'version': '2.0',
		'resultCode': 'OK',
		'output': {
			'meal' : 'meal'
			}
		}
	return json.dumps(resp, ensure_ascii=False, indent=4)



app.run(host='0.0.0.0', port=3389)


