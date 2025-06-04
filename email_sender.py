import os, base64, json
from config import SCOPES
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = SCOPES
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")
TOKEN = os.getenv("TOKEN")

class GmailWebClient:
    def __init__(self, token_path='token.json', credentials_path='credentials.json', redirect_uri=None):
        self.token_path = token_path
        self.credentials_path = credentials_path
        self.redirect_uri = redirect_uri or os.getenv("REDIRECT_URI", "http://localhost:8080/callback")
        self.creds = self._autenticar()
        self.service = build('gmail', 'v1', credentials=self.creds)

        # Try to authenticate, but don't fail if credentials aren't ready
        try:
            self.creds = self._autenticar()
            self.service = build('gmail', 'v1', credentials=self.creds)
        except ValueError as e:
            # Store the error for later reference but don't fail initialization
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
            # Para aplicaciones web, no podemos hacer autorización automática
            # El usuario debe usar obtener_url_autorizacion() e intercambiar_codigo_por_token()
            raise ValueError(
                "No hay credenciales válidas. Use obtener_url_autorizacion() "
                "para obtener la URL de autorización y luego "
                "intercambiar_codigo_por_token() con el código recibido."
            )
        return creds

    def enviar_correo(self, destinatario, nombre, factura, fecha, monto, dias):
        """Envía un correo de recordatorio de pago usando la API de Gmail."""
        msg = MIMEMultipart()
        msg["To"] = destinatario
        msg["Cc"] = "juan.novelo@lapzo.com"
        msg["Subject"] = f"Recordatorio de pago - Factura {factura}"

        cuerpo = f""" 
<p>Buen día <b>{nombre}</b>,</p>

<p>¡Espero que se encuentren muy bien!</p>

<p>Les escribo para recordarle amablemente que la factura <b>{factura}</b> con fecha de vencimiento <b>{fecha}</b>, aún no ha sido pagada.<br>
El importe pendiente es de <b>${monto}</b> MXN.<br>
Según nuestros registros, la factura venció hace <b>{dias}</b> días. Le agradeceríamos que pudiera realizar el pago lo antes posible.<br><br>

Puede realizar dicho pago mediante transferencia bancaria a la siguiente cuenta:<br><br>
<i><b>Banco:</b> Banamex<br>
<b>Sucursal:</b> 861 C F SAN PEDRO NL<br>
<b>Dirección:</b> RIO JORDAN #100 DEL VALLE<br>
<b>Cuenta de Cheques:</b> 8012426210<br>
<b>CLABE Interbancaria:</b> 002580700953579529<br>
<b>Referencia o concepto de pago:</b> {factura}</i><br><br>

<b>**Si ya ha realizado anteriormente la transacción, favor de compartir el comprobante de pago.**</b><br><br>

Si tiene alguna pregunta o necesita ayuda, no dude en ponerse en contacto con nosotros.<br><br>

¡Muchas gracias por su atención!<br>
Saludos.</p>
        """

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


