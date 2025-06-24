import os, base64, json
from config import SCOPES
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email_template import *

SCOPES = SCOPES
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")
CORREO_COPIA = "juan.novelo@lapzo.com, jesus.fernando@lapzo.com"
TOKEN = os.getenv("TOKEN")

class GmailWebClient:
    def __init__(self, token_path='token.json', credentials_path='credentials.json', redirect_uri=None):
        self.token_path = token_path
        self.credentials_path = credentials_path
        self.redirect_uri = redirect_uri or os.getenv("REDIRECT_URI", "http://localhost:8080/callback")
        self.creds = self._autenticar()
        self.service = build('gmail', 'v1', credentials=self.creds)

        try:
            self.creds = self._autenticar()
            self.service = build('gmail', 'v1', credentials=self.creds)
        except ValueError as e:
            self._auth_error = str(e)
            print(f"Gmail authentication not ready: {e}")
        except Exception as e:
            self._auth_error = f"Unexpected error: {str(e)}"
            print(f"Gmail initialization error: {e}")

    def is_authenticated(self):
        """Check if Gmail is properly authenticated and ready to use."""
        return self.service is not None and self.creds is not None

    def get_auth_status(self):
        """Get authentication status for debugging."""
        if self.is_authenticated():
            return "Authenticated and ready"
        elif hasattr(self, '_auth_error'):
            return f"Not authenticated: {self._auth_error}"
        else:
            return "Authentication status unknown"

    def _guardar_credentials_json(self):
        """Guarda las credenciales JSON desde la variable de entorno."""
        if os.path.exists(self.credentials_path):
            return  # Ya existe, no sobrescribas
        creds_str = os.getenv("GOOGLE_CREDENTIALS")
        if not creds_str:
            raise ValueError("GOOGLE_CREDENTIALS no está definida")
        with open(self.credentials_path, "w") as f:
            json.dump(json.loads(creds_str), f)

    def _guardar_token_json(self):
        """Guarda el token JSON desde la variable de entorno."""
        if os.path.exists(self.token_path):
            return True  # Ya existe
        token_str = os.getenv("TOKEN")
        if not token_str:
            return False
        with open(self.token_path, "w") as f:
            json.dump(json.loads(token_str), f)
        return True

    def _cargar_credenciales(self):
        """Carga credenciales desde el archivo token.json si existen y son válidas."""
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            if creds and creds.valid:
                return creds
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    # Guardar las credenciales actualizadas
                    with open(self.token_path, 'w') as token_file:
                        token_file.write(creds.to_json())
                    return creds
                except Exception as e:
                    print(f"Error al refrescar token: {e}")
                    return None
        return None

    def obtener_url_autorizacion(self):
        """Genera la URL de autorización para aplicaciones web."""
        self._guardar_credentials_json()
        flow = Flow.from_client_secrets_file(
            self.credentials_path,
            SCOPES,
            redirect_uri=self.redirect_uri
        )
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'  # Fuerza el consent para obtener refresh_token
        )
        return auth_url, flow

    def intercambiar_codigo_por_token(self, authorization_code):
        """Intercambia el código de autorización por tokens de acceso."""
        self._guardar_credentials_json()
        flow = Flow.from_client_secrets_file(
            self.credentials_path,
            SCOPES,
            redirect_uri=self.redirect_uri
        )
        flow.fetch_token(code=authorization_code)
        creds = flow.credentials

        # Guardar las credenciales
        with open(self.token_path, 'w') as token_file:
            token_file.write(creds.to_json())

        return creds

    def _autenticar(self):
        """Autentica y devuelve las credenciales."""
        if not os.path.exists(self.token_path):
            self._guardar_token_json()  # Crea token.json desde la variable TOKEN si existe

        creds = self._cargar_credenciales()
        if not creds:
            
            raise ValueError(
                "No hay credenciales válidas. Use obtener_url_autorizacion() "
                "para obtener la URL de autorización y luego "
                "intercambiar_codigo_por_token() con el código recibido."
            )
        return creds

    def enviar_correo(self, destinatario, nombre, factura, fecha, monto, moneda, dias, url=None):
        """Envía un correo de recordatorio de pago usando la API de Gmail."""
        msg = MIMEMultipart()
        # Manejar múltiples destinatarios principales
        if isinstance(destinatario, str):
            # Si es string, puede contener múltiples emails separados por comas
            destinatarios_principales = [email.strip() for email in destinatario.split(',') if email.strip()]
        elif isinstance(destinatario, list):
            # Si es lista, tomar cada elemento
            destinatarios_principales = [email.strip() for email in destinatario if email.strip()]
        else:
            destinatarios_principales = [str(destinatario)]
        
        if not destinatarios_principales:
            print("❌ No se proporcionaron destinatarios válidos")
            return False
        
        # Establecer destinatarios principales
        msg["To"] = ", ".join(destinatarios_principales)
        print(f"📧 Enviando a destinatarios principales: {', '.join(destinatarios_principales)}")
            
        # Manejar múltiples correos en copia correctamente
        if CORREO_COPIA:
            # Si CORREO_COPIA tiene múltiples correos, asegurar formato correcto
            correos_copia = [email.strip() for email in CORREO_COPIA.split(',') if email.strip()]
            if correos_copia:  # Solo agregar Cc si hay correos válidos
                msg["Cc"] = ", ".join(correos_copia)
                print(f"📋 Enviando copia a: {', '.join(correos_copia)}")
        
        msg["Subject"] = f"Recordatorio de pago - Factura {factura}"

        if moneda == 'USD':
            cuerpo = generar_correo_usd(nombre, factura, fecha, monto, moneda, dias, url)
        else:
            cuerpo = generar_correo_mxn(nombre, factura, fecha, monto, moneda, dias, url)
            
        msg.attach(MIMEText(cuerpo, "html"))
        
        mensaje_encoded = {
            'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()
        }

        try:
            enviado = self.service.users().messages().send(userId="me", body=mensaje_encoded).execute()
            print(f"📧 Correo enviado a {destinatario} con la factura {factura} (ID: {enviado['id']})")
            return True
        except HttpError as e:
            print(f"❌ Error de API al enviar correo a {destinatario}: {e}")
            return False
        except Exception as e:
            print(f"❌ Error al enviar correo a {destinatario}: {e}")
            return False


