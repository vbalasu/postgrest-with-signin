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
    return (jwt.encode(token_data, mysecrets.PGRST_JWT_SECRET, algorithm='HS256').decode('utf8'), token_data)

@app.route('/')
def index():
    return jsonify(trade_in(request.args.get("token")))
