import json
import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Configuración del alcance (Permisos para leer y escribir en Drive y Sheets)
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_flow():
    """Prepara el flujo de autenticación leyendo el secreto"""
    client_config = os.getenv("GOOGLE_CLIENT_SECRET_JSON")
    client_config_dict = json.loads(client_config)
    return Flow.from_client_config(client_config_dict, scopes=SCOPES)
    

def generar_link_auth():
    """Genera el link para que el usuario haga clic"""
    flow = get_flow()
    # Esta URL especial le dice a Google "Muestra el código en pantalla"
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    return auth_url

def intercambiar_codigo_por_token(codigo_usuario):
    """Recibe el código que pegó el usuario y devuelve las credenciales finales"""
    flow = get_flow()
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    
    # Intercambia el código por tokens reales
    flow.fetch_token(code=codigo_usuario)
    creds = flow.credentials
    
    # Convertimos las credenciales a JSON para guardarlas en la BD
    creds_json = creds.to_json()
    return creds_json

def obtener_creds_desde_json(json_text):
    """Reconstruye el objeto Credentials desde el texto guardado en BD"""
    if not json_text:
        return None
    creds = Credentials.from_authorized_user_info(json.loads(json_text), SCOPES)
    return creds