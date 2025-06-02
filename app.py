from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash
from odoo_connector import OdooConnector
from email_sender import GmailWebClient

import os, time, threading, logging

# Configuración básica
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY_FLASK")
logging.basicConfig(level=logging.INFO)


# Clase orientada a objetos para encapsular la lógica de facturas
class InvoiceApp:
    def __init__(self):
        self.odoo = OdooConnector()
        self.gmail = None
        self._gmail_initialized = False

    def _inicializar_gmail(self):
        """Inicializa Gmail solo cuando sea necesario"""
        if not self._gmail_initialized:
            try:
                self.gmail = GmailWebClient()
                # Check if it's actually authenticated
                if self.gmail.is_authenticated():
                    self._gmail_initialized = True
                    return True
                else:
                    logging.warning(f"Gmail creado pero no autenticado: {self.gmail.get_auth_status()}")
                    return False
            except Exception as e:
                logging.warning(f"Error al inicializar Gmail: {e}")
                self.gmail = None
                return False
        return self.gmail is not None and self.gmail.is_authenticated()

    def verificar_autorizacion_gmail(self):
        """Verifica si Gmail está autorizado"""
        if not self._gmail_initialized:
            self._inicializar_gmail()

        return self.gmail is not None and self.gmail.is_authenticated()

    def obtener_facturas_vencidas(self):
        facturas = self.odoo.get_overdue_invoices()
        for factura in facturas:
            factura['dias_vencido'] = self.odoo.calcular_dias_vencimiento(factura['invoice_date_due'])
        return facturas

    def enviar_recordatorio(self, factura_id):
        if not self._inicializar_gmail():
            flash("Gmail no está configurado o autorizado correctamente", "error")
            return False

        facturas = self.odoo.get_overdue_invoices()
        factura = next((f for f in facturas if str(f['id']) == factura_id), None)

        if not factura:
            logging.warning(f"Factura no encontrada: {factura_id}")
            flash("Factura no encontrada.", "error")
            return False

        cliente_id, cliente_nombre = factura['partner_id']
        cliente = self.odoo.get_customer_data(cliente_id)

        if not cliente or not cliente.get('email'):
            flash(f"No se encontró email para {cliente_nombre}", "error")
            return False

        try:
            enviado = self.gmail.enviar_correo(
                destinatario='fjesusandre@gmail.com',  # cliente['email'],
                nombre=cliente['name'],
                factura=factura['name'],
                fecha=factura['invoice_date_due'],
                monto=factura['amount_total'],
                dias=self.odoo.calcular_dias_vencimiento(factura['invoice_date_due'])
            )

            if enviado:
                flash(f"Correo enviado a {cliente['email']}", "success")
            else:
                flash("Error al enviar el correo.", "error")

            return True

        except ValueError as e:
            # Gmail authentication error
            logging.error(f"Error de autenticación Gmail: {str(e)}")
            flash("Gmail no está autorizado. Vaya a 'Autorizar Gmail' primero.", "error")
            return False

        except Exception as e:
            logging.error(f"Error al enviar correo: {str(e)}")
            flash(f"Error al enviar correo: {str(e)}", "error")
            return False

    def enviar_recordatorios_masivos_custom(self, facturas_a_enviar):
        if not self._inicializar_gmail():
            flash("Gmail no autorizado", "error")
            return {
                'exitosos': 0,
                'fallidos': 0,
                'sin_email': 0,
                'detalles': []
            }

        resultados = {
            'exitosos': 0,
            'fallidos': 0,
            'sin_email': 0,
            'detalles': []
        }

        for factura in facturas_a_enviar:
            cliente_id, cliente_nombre = factura['partner_id']
            cliente = self.odoo.get_customer_data(cliente_id)

            if not cliente or not cliente.get('email'):
                resultados['sin_email'] += 1
                resultados['detalles'].append({
                    'cliente': cliente_nombre,
                    'factura': factura['name'],
                    'estado': 'Sin email'
                })
                continue

            try:
                enviado = self.gmail.enviar_correo(
                    destinatario='fjesusandre@gmail.com',  # cliente['email'],
                    nombre=cliente['name'],
                    factura=factura['name'],
                    fecha=factura['invoice_date_due'],
                    monto=factura['amount_total'],
                    dias=factura['dias_vencido']
                )

                if enviado:
                    resultados['exitosos'] += 1
                    resultados['detalles'].append({
                        'cliente': cliente_nombre,
                        'factura': factura['name'],
                        'estado': 'Enviado'
                    })
                else:
                    resultados['fallidos'] += 1
                    resultados['detalles'].append({
                        'cliente': cliente_nombre,
                        'factura': factura['name'],
                        'estado': 'Error al enviar'
                    })

                time.sleep(1)

            except Exception as e:
                resultados['fallidos'] += 1
                resultados['detalles'].append({
                    'cliente': cliente_nombre,
                    'factura': factura['name'],
                    'estado': f'Error: {str(e)}'
                })

        return resultados

    def enviar_recordatorios_masivos(self, modo="todos"):
        """
        Envía recordatorios a múltiples clientes
        modo: "todos", "seleccionados" (lista de IDs), o filtros específicos
        """
        facturas = self.obtener_facturas_vencidas()

        if modo == "todos":
            facturas_a_enviar = facturas
        else:
            # Aquí puedes agregar otros filtros
            facturas_a_enviar = facturas

        resultados = {
            'exitosos': 0,
            'fallidos': 0,
            'sin_email': 0,
            'detalles': []
        }

        for factura in facturas_a_enviar:
            cliente_id, cliente_nombre = factura['partner_id']
            cliente = self.odoo.get_customer_data(cliente_id)

            if not cliente or not cliente.get('email'):
                resultados['sin_email'] += 1
                resultados['detalles'].append({
                    'cliente': cliente_nombre,
                    'factura': factura['name'],
                    'estado': 'Sin email'
                })
                continue

            try:
                enviado = self.gmail.enviar_correo(
                    destinatario='fjesusandre@gmail.com',  # cliente['email'],
                    nombre=cliente['name'],
                    factura=factura['name'],
                    fecha=factura['invoice_date_due'],
                    monto=factura['amount_total'],
                    dias=self.odoo.calcular_dias_vencimiento(factura['invoice_date_due'])
                )

                if enviado:
                    resultados['exitosos'] += 1
                    resultados['detalles'].append({
                        'cliente': cliente_nombre,
                        'factura': factura['name'],
                        'email': cliente['email'],
                        'estado': 'Enviado'
                    })
                else:
                    resultados['fallidos'] += 1
                    resultados['detalles'].append({
                        'cliente': cliente_nombre,
                        'factura': factura['name'],
                        'email': cliente['email'],
                        'estado': 'Error al enviar'
                    })

                # Pausa pequeña entre envíos para evitar límites de rate
                time.sleep(1)


            except ValueError as e:

                # Gmail authentication error

                logging.error(f"Error de autenticación Gmail para {cliente_nombre}: {str(e)}")

                resultados['fallidos'] += 1

                resultados['detalles'].append({

                    'cliente': cliente_nombre,

                    'factura': factura['name'],

                    'email': cliente.get('email', 'N/A'),

                    'estado': 'Gmail no autorizado'

                })

                break  # Stop trying if Gmail isn't authorized

            except Exception as e:

                logging.error(f"Error enviando a {cliente_nombre}: {str(e)}")

                resultados['fallidos'] += 1

                resultados['detalles'].append({

                    'cliente': cliente_nombre,

                    'factura': factura['name'],

                    'email': cliente.get('email', 'N/A'),

                    'estado': f'Error: {str(e)}'

                })


# Crear una instancia del manejador
invoice_app = InvoiceApp()


# Rutas de Flask que delegan en la clase
@app.route('/')
def index():
    facturas = invoice_app.obtener_facturas_vencidas()
    desde = request.args.get("desde", type=int)
    hasta = request.args.get("hasta", type=int)
    cliente = request.args.get("cliente", "").lower()

    if desde is not None:
        facturas = [f for f in facturas if f['dias_vencido'] >= desde]
    if hasta is not None:
        facturas = [f for f in facturas if f['dias_vencido'] <= hasta]
    if cliente:
        facturas = [f for f in facturas if cliente in f['partner_id'][1].lower()]

    return render_template('index.html', facturas=facturas)


@app.route('/enviar/<factura_id>')
def enviar(factura_id):
    invoice_app.enviar_recordatorio(factura_id)
    return redirect(url_for('index'))


@app.route('/enviar-todos')
def enviar_todos():
    """Envía correos a todos los clientes con facturas vencidas"""
    desde = request.args.get("desde", type=int)
    hasta = request.args.get("hasta", type=int)
    cliente = request.args.get("cliente", "").lower()
    facturas = invoice_app.obtener_facturas_vencidas()

    if desde is not None:
        facturas = [f for f in facturas if f['dias_vencido'] >= desde]
    if hasta is not None:
        facturas = [f for f in facturas if f['dias_vencido'] <= hasta]
    if cliente:
        facturas = [f for f in facturas if cliente in f['partner_id'][1].lower()]

    try:
        resultados = invoice_app.enviar_recordatorios_masivos_custom(facturas)
        flash(
            f"Envío masivo completado: {resultados['exitosos']} exitosos, {resultados['fallidos']} fallidos, {resultados['sin_email']} sin email",
            "success")
    except Exception as e:
        flash(f"Error en envío masivo: {str(e)}", "error")

    return redirect(url_for('index'))


# Nuevas rutas para manejar la autorización de Google OAuth2
@app.route('/autorizar-gmail')
def autorizar_gmail():
    """Inicia el proceso de autorización de Gmail"""
    try:
        # Crear una instancia temporal para obtener la URL de autorización
        gmail_temp = GmailWebClient.__new__(GmailWebClient)
        gmail_temp.credentials_path = 'credentials.json'
        gmail_temp.token_path = 'token.json'
        gmail_temp.redirect_uri = url_for('gmail_callback', _external=True)

        auth_url, _ = gmail_temp.obtener_url_autorizacion()
        return redirect(auth_url)

    except Exception as e:
        flash(f"Error al iniciar autorización: {str(e)}", "error")
        return redirect(url_for('index'))


@app.route('/gmail/callback')
def gmail_callback():
    """Maneja la respuesta de autorización de Google"""
    try:
        # Obtener el código de autorización
        code = request.args.get('code')
        if not code:
            flash("No se recibió código de autorización", "error")
            return redirect(url_for('index'))

        # Crear una instancia temporal para intercambiar el código
        gmail_temp = GmailWebClient.__new__(GmailWebClient)
        gmail_temp.credentials_path = 'credentials.json'
        gmail_temp.token_path = 'token.json'
        gmail_temp.redirect_uri = url_for('gmail_callback', _external=True)

        # Intercambiar código por tokens
        gmail_temp.intercambiar_codigo_por_token(code)

        # Reinicializar la instancia de Gmail en la aplicación
        invoice_app._gmail_initialized = False
        invoice_app.gmail = None

        flash("Gmail autorizado exitosamente", "success")

    except Exception as e:
        flash(f"Error en la autorización: {str(e)}", "error")

    return redirect(url_for('index'))


@app.route('/estado-gmail')
def estado_gmail():
    """Muestra el estado de autorización de Gmail"""
    autorizado = invoice_app.verificar_autorizacion_gmail()

    if autorizado:
        mensaje = "Gmail está autorizado y listo para enviar correos"
        categoria = "success"
    else:
        mensaje = "Gmail no está autorizado. Haz clic en 'Autorizar Gmail' para configurarlo"
        categoria = "warning"

    flash(mensaje, categoria)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)