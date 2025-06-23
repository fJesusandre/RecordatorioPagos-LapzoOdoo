from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from odoo_connector import OdooConnector
from email_sender import GmailWebClient
import os, time, threading, logging

load_dotenv()

# Configuración básica
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY_FLASK")
logging.basicConfig(level=logging.INFO)
ODOO_URL = os.getenv("ODOO_URL")

# Configuración de usuario único para login
USERNAME = os.getenv("ADMIN_USERNAME")  # Usuario desde .env o 'admin' por defecto
PASSWORD_HASH = generate_password_hash(os.getenv("ADMIN_PASSWORD"))  # Contraseña desde .env

def login_required(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Debes iniciar sesión para acceder', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Clase orientada a objetos para encapsular la lógica de facturas (sin cambios)
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
        
        try:
            factura_id_int = int(factura_id)
        except (ValueError, TypeError):
            logging.warning(f"ID de factura inválido: {factura_id}")
            flash("ID de factura inválido.", "error")
            return False
        
        # Buscar por ID entero
        factura = next((f for f in facturas if f['id'] == factura_id_int), None)

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
                destinatario=cliente['email'],
                nombre=cliente['name'],
                factura=factura['name'],
                fecha=factura['invoice_date_due'],
                monto=factura['amount_residual'],
                moneda=factura['currency_id'][1],
                dias=self.odoo.calcular_dias_vencimiento(factura['invoice_date_due']),
                url=f"{ODOO_URL}/my/invoices/{factura['id']}?access_token={factura['access_token']}"
            )

            if enviado:
                flash(f"Correo enviado a {cliente['email']}", "success")
            else:
                flash("Error al enviar el correo.", "error")

            return True

        except ValueError as e:
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
                    destinatario=cliente['email'],
                    nombre=cliente['name'],
                    factura=factura['name'],
                    fecha=factura['invoice_date_due'],
                    monto=factura['amount_residual'],
                    moneda=factura['currency_id'][1],
                    dias=self.odoo.calcular_dias_vencimiento(factura['invoice_date_due']),
                    url=f"{ODOO_URL}/my/invoices/{factura['id']}?access_token={factura['access_token']}"
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
                    destinatario=cliente['email'],
                    nombre=cliente['name'],
                    factura=factura['name'],
                    fecha=factura['invoice_date_due'],
                    monto=factura['amount_residual'],
                    moneda=factura['currency_id'][1],
                    dias=self.odoo.calcular_dias_vencimiento(factura['invoice_date_due']),
                    url=f"{ODOO_URL}/my/invoices/{factura['id']}?access_token={factura['access_token']}"
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
                logging.error(f"Error de autenticación Gmail para {cliente_nombre}: {str(e)}")
                resultados['fallidos'] += 1
                resultados['detalles'].append({
                    'cliente': cliente_nombre,
                    'factura': factura['name'],
                    'email': cliente.get('email', 'N/A'),
                    'estado': 'Gmail no autorizado'
                })
                break  

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


# RUTAS DE AUTENTICACIÓN


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está logueado, redirigir al dashboard
    if session.get('logged_in'):
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
            session['logged_in'] = True
            session['username'] = username
            flash('Acceso autorizado', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))


# RUTAS PRINCIPALES (PROTEGIDAS)


@app.route('/')
@login_required
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

@app.route('/enviar/<int:factura_id>', methods=['GET', 'POST'])
@login_required
def enviar(factura_id):
    """Envía recordatorio a una factura específica"""
    try:
        # Verificar que la factura existe y está vencida
        facturas = invoice_app.obtener_facturas_vencidas()
        factura = next((f for f in facturas if f['id'] == factura_id), None)
        
        if not factura:
            flash(f"Factura {factura_id} no encontrada o no está vencida", "error")
            return redirect(url_for('index'))
        
        # Enviar el recordatorio
        resultado = invoice_app.enviar_recordatorio(str(factura_id))
        
        if resultado:
            flash(f"Recordatorio enviado exitosamente a {factura['partner_id'][1]}", "success")
        else:
            flash(f"Error al enviar recordatorio a {factura['partner_id'][1]}", "error")
            
    except Exception as e:
        flash(f"Error al enviar recordatorio: {str(e)}", "error")
    
    return redirect(url_for('index'))

@app.route('/enviar-todos', methods=['GET', 'POST'])
@login_required
def enviar_todos():
    """Envía correos a clientes seleccionados con facturas vencidas"""
    try:
        if request.method == 'POST':
            # Obtener los IDs de facturas seleccionadas del formulario
            facturas_ids = request.form.getlist('facturas_ids')
            facturas_ids = [int(id) for id in facturas_ids if id.isdigit()]
            
            if not facturas_ids:
                flash("No se seleccionaron facturas para enviar", "warning")
                return redirect(url_for('index'))
            
            # Obtener todas las facturas vencidas
            todas_facturas = invoice_app.obtener_facturas_vencidas()
            
            # Filtrar solo las facturas seleccionadas
            facturas_seleccionadas = [f for f in todas_facturas if f['id'] in facturas_ids]
            
            if not facturas_seleccionadas:
                flash("Las facturas seleccionadas no están disponibles", "error")
                return redirect(url_for('index'))
            
        else:
            desde = request.args.get("desde", type=int)
            hasta = request.args.get("hasta", type=int)
            cliente = request.args.get("cliente", "").lower()
            facturas_seleccionadas = invoice_app.obtener_facturas_vencidas()

            # Aplicar filtros
            if desde is not None:
                facturas_seleccionadas = [f for f in facturas_seleccionadas if f['dias_vencido'] >= desde]
            if hasta is not None:
                facturas_seleccionadas = [f for f in facturas_seleccionadas if f['dias_vencido'] <= hasta]
            if cliente:
                facturas_seleccionadas = [f for f in facturas_seleccionadas if cliente in f['partner_id'][1].lower()]

        # Enviar recordatorios masivos
        resultados = invoice_app.enviar_recordatorios_masivos_custom(facturas_seleccionadas)
        
        # Mostrar resultados
        mensaje_exito = f"Envío masivo completado: {resultados['exitosos']} exitosos"
        if resultados['fallidos'] > 0:
            mensaje_exito += f", {resultados['fallidos']} fallidos"
        if resultados['sin_email'] > 0:
            mensaje_exito += f", {resultados['sin_email']} sin email"
            
        flash(mensaje_exito, "success")
        
        # Mostrar detalles si hay errores
        if resultados.get('errores'):
            for error in resultados['errores'][:5]:  # Mostrar solo los primeros 5 errores
                flash(f"Error: {error}", "error")
        
    except Exception as e:
        flash(f"Error en envío masivo: {str(e)}", "error")

    return redirect(url_for('index'))

@app.route('/api/facturas-estado', methods=['GET'])
@login_required
def facturas_estado():
    """API para obtener el estado actual de las facturas (para actualizaciones AJAX)"""
    try:
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

        # Devolver solo los IDs y nombres para verificación
        facturas_info = [
            {
                'id': f['id'],
                'name': f['name'],
                'partner_name': f['partner_id'][1],
                'dias_vencido': f['dias_vencido']
            } 
            for f in facturas
        ]
        
        return jsonify({
            'facturas': facturas_info,
            'total': len(facturas_info)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/validar-facturas', methods=['POST'])
@login_required
def validar_facturas():
    """Valida que las facturas seleccionadas están disponibles para envío"""
    try:
        data = request.get_json()
        facturas_ids = data.get('facturas_ids', [])
        
        if not facturas_ids:
            return jsonify({'valid': False, 'message': 'No se proporcionaron IDs de facturas'})
        
        # Obtener facturas actuales
        facturas_actuales = invoice_app.obtener_facturas_vencidas()
        ids_actuales = [f['id'] for f in facturas_actuales]
        
        # Verificar cuáles IDs son válidos
        ids_validos = [id for id in facturas_ids if id in ids_actuales]
        ids_invalidos = [id for id in facturas_ids if id not in ids_actuales]
        
        return jsonify({
            'valid': len(ids_invalidos) == 0,
            'ids_validos': ids_validos,
            'ids_invalidos': ids_invalidos,
            'total_validos': len(ids_validos),
            'message': f'{len(ids_validos)} facturas válidas, {len(ids_invalidos)} inválidas'
        })
        
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500

@app.route('/autorizar-gmail')
@login_required
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
@login_required
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
@login_required
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
    print(f"=== Sistema de Facturas con Autenticación ===")
    print(f"Usuario: {USERNAME}")
    print("Contraseña: Configurada desde variables de entorno")
    print("Accede a: http://localhost:5000")
    app.run(debug=True)