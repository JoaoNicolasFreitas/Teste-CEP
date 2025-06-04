# 🔍 Consulta CEP Web

Projeto web desenvolvido com **Python (Django)**, **HTML** e **CSS**, que permite ao usuário consultar um CEP, visualizar a localização no mapa, copiar e compartilhar as informações. Foi realizado teste de estresse com **JMeter** no endpoint `/ws/44245000/json/`.

---

## 🚀 Tecnologias Utilizadas

- Python 3.x
- Django
- HTML5
- CSS3
- [ViaCEP API](https://viacep.com.br/)
- Google Maps Embed API
- JMeter (para teste de estresse)

---

## 💡 Funcionalidades

- Consulta de CEP em tempo real.
- Exibição dos dados (logradouro, bairro, cidade, estado).
- Visualização no mapa da cidade correspondente ao CEP.
- Botão para copiar os dados da consulta.
- Botão para compartilhar as informações.
- Teste de estresse com JMeter no endpoint `/ws/44245000/json/`.

---

## 🧪 Testes de Estresse (JMeter)

O endpoint `/ws/44245000/json/` foi testado com **Apache JMeter** para avaliar desempenho e resistência sob carga.

**Parâmetros do teste:**
- Threads (Usuários Virtuais): 2000
- Tempo de ramp-up: 10 segundos
- Requisições por segundo: configuradas com loop
- Duração: 1 minuto

## 🖼️ Demonstração

![Demonstração do Projeto](essas no projeto nas imagens)

---

## ⚙️ Como Executar o Projeto

```bash
# Clone o repositório
git clone https://github.com/JoaoNicolasFreitas/Teste-CEP.git
cd nome-do-repo

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Rode o servidor
python manage.py runserver
