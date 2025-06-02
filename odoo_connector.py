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
            common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
            self.uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_API_KEY, {})
            if not self.uid:
                logger.error("Autenticación fallida. Verifica las credenciales.")
                return False
            self.models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
            logger.info("Conexión exitosa a Odoo")
            return True
        except Exception as e:
            logger.exception("Error al conectar con Odoo")
            print(e)
            return False

    def get_overdue_invoices(self, due_date=None):
        """Obtiene facturas vencidas."""
        if not self.connected:
            return []

        due_date = due_date or date.today().strftime('%Y-%m-%d')

        domain = [
            ('move_type', '=', 'out_invoice'),
            ('invoice_date_due', '<', due_date),
            ('payment_state', '!=', 'paid')
        ]
        fields = ['name', 'partner_id', 'amount_total', 'invoice_date_due', 'invoice_date']

        try:
            return self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_API_KEY,
                'account.move', 'search_read',
                [domain],
                {'fields': fields}
            )
        except Exception as e:
            logger.exception("Error al obtener facturas vencidas")
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
