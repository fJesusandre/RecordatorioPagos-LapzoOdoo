import xmlrpc.client
import logging
import os
from datetime import date,datetime

ODOO_URL = os.getenv("ODOO_URL")
ODOO_API_KEY = os.getenv("ODOO_API_KEY")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USER = os.getenv("ODOO_USER")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OdooConnector:
    def __init__(self):
        self.uid = None
        self.models = None
        self.connected = self.connect()

    def connect(self):
        """Establece conexión con el servidor Odoo."""
        try:
            logger.info(f"Conectando a {ODOO_URL}...")

            # Uso de transporte seguro para HTTPS
            transport = xmlrpc.client.SafeTransport()

            common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common", transport=transport)
            self.uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_API_KEY, {})
            if not self.uid:
                logger.error("Autenticación fallida. Verifica las credenciales.")
                return False
            self.models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object", transport=transport)
            logger.info("Conexión exitosa a Odoo")
            return True
        except Exception as e:
            logger.exception("Error al conectar con Odoo")
            print(e)
            return False

    def get_overdue_invoices(self, due_date=None):
        
        if not self.connected:
            return []

        due_date = due_date or date.today().strftime('%Y-%m-%d')
        cuentas_validas = ['1', '5', '6']  # Como strings

        try:
            # Buscar líneas que tengan distribución analítica con nuestras cuentas
            domain_lineas = [
                ('move_id.move_type', '=', 'out_invoice'),
                ('move_id.invoice_date_due', '<', due_date),
                ('move_id.payment_state', '!=', 'paid'),
                ('move_id.state', '=', 'posted'),
                ('analytic_distribution', '!=', False)
            ]

            lineas = self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_API_KEY,
                'account.move.line', 'search_read',
                [domain_lineas],
                {'fields': ['move_id', 'analytic_distribution']}
            )

            logger.info(f"Líneas encontradas con distribución analítica: {len(lineas)}")

            # Filtrar las que tienen nuestras cuentas (las claves son strings)
            facturas_validas = set()
            for linea in lineas:
                if linea.get('analytic_distribution'):
                    # Las claves son strings {'6': 100.0}, {'5': 100.0}
                    claves_distribucion = linea['analytic_distribution'].keys()
                    if any(clave in cuentas_validas for clave in claves_distribucion):
                        facturas_validas.add(linea['move_id'][0])

            logger.info(f"Facturas válidas encontradas: {len(facturas_validas)}")

            if not facturas_validas:
                return []

            # Obtener datos completos de las facturas válidas
            factura_fields = [
                'id', 'name', 'partner_id', 'currency_id',
                'amount_residual_signed', 'amount_residual',
                'invoice_date_due', 'invoice_date',
                'access_token'
            ]

            facturas = self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_API_KEY,
                'account.move', 'read',
                [list(facturas_validas)],
                {'fields': factura_fields}
            )

            logger.info(f"Retornando {len(facturas)} facturas con cuentas analíticas válidas")
            return facturas

        except Exception:
            logger.exception("Error en método optimizado final")
            return []


    def get_customer_data(self, customer_id):
        """Obtiene datos completos del cliente."""
        if not self.connected:
            return None
        try:
            result = self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_API_KEY,
                'res.partner', 'read',
                [customer_id],
                {'fields': ['email', 'name', 'phone', 'mobile', 'city', 'vat']}
            )
            return result[0] if result else None
        except Exception as e:
            logger.warning(f"No se pudo obtener cliente {customer_id}")
            logger.debug(e)
            return None

    @staticmethod
    def calcular_dias_vencimiento(fecha_vencimiento):
        """Calcula los días de vencimiento dados una fecha."""
        fecha_actual = date.today()
        if isinstance(fecha_vencimiento, str):
            fecha_venc = datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
        else:
            fecha_venc = fecha_vencimiento
        dias = (fecha_actual - fecha_venc).days
        return dias if dias > 0 else 0
