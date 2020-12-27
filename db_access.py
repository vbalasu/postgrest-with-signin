from flask import Flask, request, jsonify
import mysecrets
import jwt

app = Flask(__name__)

def verify(token):
  from google.oauth2 import id_token
  from google.auth.transport import requests
  # (Receive token by HTTPS POST)
  # ...
  try:
      # Specify the CLIENT_ID of the app that accesses the backend:
      idinfo = id_token.verify_oauth2_token(token, requests.Request(), mysecrets.GOOGLE_CLIENT_ID)
      # Or, if multiple clients access the backend server:
      # idinfo = id_token.verify_oauth2_token(token, requests.Request())
      # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
      #     raise ValueError('Could not verify audience.')
      if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
          raise ValueError('Wrong issuer.')
      # If auth request is from a G Suite domain:
      # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
      #     raise ValueError('Wrong hosted domain.')
      # ID token is valid. Get the user's Google Account ID from the decoded token.
      userid = idinfo['sub']
      return idinfo
  except ValueError:
    return False

# Trade in Google token for db token
def trade_in(id_token):
    token_data = verify(id_token)
    del token_data['aud']
    token_data['role'] = 'user_' + token_data['sub']
    return jwt.encode(token_data, mysecrets.PGRST_JWT_SECRET, algorithm='HS256')

def create_role(id_token):
    token_data = verify(id_token)
    print(token_data)
    if token_data:
        role = 'user_' + token_data['sub']
        import psycopg2
        conn = psycopg2.connect(host='postgres.amer.trifacta.net', dbname='main', user='trifacta', password=mysecrets.POSTGRES_PASSWORD)
        cur = conn.cursor()
        cur.callproc('create_role', (role,))
        conn.commit()
        conn.close()
        return 'role created: ' + role
    else:
        return 'error'

@app.route('/')
def index():
    return 'Missing command'

@app.route('/swap')
def swap():
    if not request.args.get("token"):
        return 'Missing token'
    else:
        return trade_in(request.args.get("token"))

@app.route('/create_role')
def route_create_role():
    if not request.args.get("token"):
        return 'Missing token'
    else:
        return create_role(request.args.get("token"))