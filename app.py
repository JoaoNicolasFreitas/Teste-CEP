from flask import Flask, render_template, request, jsonify
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

app = Flask(__name__)

# Configuração do cliente HTTP com retry
def create_http_client():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,  # número total de tentativas
        backoff_factor=0.5,  # tempo de espera entre tentativas
        status_forcelist=[500, 502, 503, 504]  # códigos de erro para tentar novamente
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consulta-cep', methods=['POST'])
def consulta_cep():
    try:
        cep = request.form.get('cep')
        if not cep:
            return jsonify({'error': 'CEP não fornecido'}), 400
        
        # Remove caracteres não numéricos
        cep = ''.join(filter(str.isdigit, cep))
        
        if len(cep) != 8:
            return jsonify({'error': 'CEP deve conter 8 dígitos'}), 400
        
        # Cria cliente HTTP com retry
        http_client = create_http_client()
        
        # Faz a requisição para o ViaCEP com timeout
        try:
            response = http_client.get(
                f'https://viacep.com.br/ws/{cep}/json/',
                timeout=5  # timeout de 5 segundos
            )
            response.raise_for_status()  # levanta exceção para códigos de erro HTTP
        except requests.Timeout:
            return jsonify({'error': 'Tempo de conexão com o ViaCEP excedido. Tente novamente.'}), 504
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return jsonify({'error': 'CEP não encontrado'}), 404
            return jsonify({'error': 'Erro ao consultar o serviço ViaCEP'}), 500
        
        data = response.json()
        
        # Verifica se o CEP existe
        if 'erro' in data:
            return jsonify({'error': 'CEP não encontrado'}), 404
            
        # Formata o CEP com hífen
        if 'cep' in data:
            data['cep'] = f"{data['cep'][:5]}-{data['cep'][5:]}"
            
        return jsonify(data)
        
    except requests.RequestException as e:
        app.logger.error(f"Erro de conexão: {str(e)}")
        return jsonify({
            'error': 'Erro de conexão com o serviço ViaCEP. Por favor, tente novamente em alguns instantes.',
            'details': 'O serviço pode estar temporariamente indisponível.'
        }), 503
    except Exception as e:
        app.logger.error(f"Erro interno: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': 'Ocorreu um erro inesperado. Por favor, tente novamente.'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 