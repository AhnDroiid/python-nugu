from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import(
	render_template,
	redirect,
	request,
	abort,
	url_for,
	session
)


@app.route('/health')
def healthCheck():
	return 'OK'


@app.route('/', methods=['POST')

def home():
	req = request.json
	print(request.json)


	return request.json












app.run(host='0.0.0.0', port=3389)



