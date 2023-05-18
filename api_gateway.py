from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from urllib import parse, request as req


app = Flask(__name__)
CORS(app)


# This simulates service data that should come from database or
# configuration file.
persistence_service = {'operation':'/persistence', 'address':'localhost', 'port':5004, 'route':'/add'}
list_service = {'operation':'/list', 'address':'localhost', 'port':5007, 'route':'/list'}


service_registry = [persistence_service , list_service]

@app.route('/api_gateway/<operation>')
def api_gateway(operation):
    for service_config in service_registry:
        if service_config['operation'] == ('/'+operation):
            parameters = {
                'str_input': request.args.get('str_input'),
                'assunto': request.args.get('assunto'),
                'autor': request.args.get('autor'),
                'a': request.args.get('a')
            }
            url = 'http://' + service_config['address'] +':' + str(service_config['port']) + service_config['route']
            if ('/'+operation) == '/persistence': # Conversion to post request
                print("Persistência...")
                data = {
                    'titulo': parameters['str_input'],
                    'assunto': parameters['assunto'],
                    'autor': parameters['autor'],
                    'data': parameters['a']
                }
                print(data)
                data_p = parse.urlencode(data).encode()
                url_request = req.urlopen(url, data=data_p)
                result = url_request.read()
            else:
                url_request = req.urlopen(url+'?'+parse.urlencode(parameters))
                result = url_request.read()
            return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)

