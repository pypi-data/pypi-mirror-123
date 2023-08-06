import logging
from datetime import datetime

from src.entities.order import Order
from src.entities.pedido import Pedido
import src
import src.database.connection as database
from src.database import queries
from src.database.utils import DatabaseConfig
import src.database.utils as utils
import src.api.okvendas as api_okvendas

logger = logging.getLogger()

default_limit = 50
queue_status = {
    'pending': 'PEDIDO',
    'paid': 'PEDIDO_PAGO',
    'shipped': 'ENCAMINHADO_ENTREGA',
    'delivered': 'ENTREGUE',
    'canceled': 'CANCELADO',
    'no_invoice': 'SEM_NOTA_FISCAL',
    'invoiced': 'FATURADO'
}


def define_job_start(job_config: dict) -> None:
    global current_job
    current_job = job_config.get('job_name')
    if current_job == 'internaliza_pedidos_job':  # Inicia o job a partir dos pedidos AgPagamento
        job_orders(job_config, True)
    else:  # Inicia o job a partir dos pedidos Confirmados
        job_orders(job_config)


def job_orders(job_config: dict, start_at_pending: bool = False) -> None:
    db_config = utils.get_database_config(job_config)
    if start_at_pending:
        process_order_queue(queue_status.get('pending'), db_config)

    process_order_queue(queue_status.get('paid'), db_config)

    process_order_queue(queue_status.get('canceled'), db_config)

    process_order_queue(queue_status.get('invoiced'), db_config)

    process_order_queue(queue_status.get('shipped'), db_config)

    process_order_queue(queue_status.get('delivered'), db_config)


def process_order_queue(status: str, db_config: DatabaseConfig) -> None:
    queue = api_okvendas.get_order_queue(
        url=src.client_data.get('url_api') + '/pedido/fila/{0}',
        token=src.client_data.get('token_api'),
        status=status,
        limit=default_limit)

    orders_to_protocol = []
    for q_order in queue:
        order = api_okvendas.get_order(
            url=src.client_data.get('url_api') + '/pedido/{0}',
            token=src.client_data.get('token_api'),
            order_id=q_order.order_id)

        if order.erp_code is not None and order.erp_code != '':
            # atualiza status do pedido no banco de dados
            if call_update_order_procedure(db_config, order):
                orders_to_protocol.append(q_order.protocol)
        else:
            # insere pedido no banco de dados
            inserted = insert_temp_order(order, db_config)
            if inserted:
                sp_success, client_erp_id, order_erp_id = call_order_procedures(db_config, q_order.order_id)
                if sp_success:
                    if api_okvendas.put_order_erp_code(src.client_data.get('url_api') + '/pedido/integradoERP', src.client_data.get('token_api'), order.order_id, order_erp_id):
                        logger.info(current_job + ' | Codigo Erp do pedido atualizado via api OkVendas')
                        orders_to_protocol.append(q_order.protocol)
                    if api_okvendas.put_client_erp_code(src.client_data.get('url_api') + '/pedido/integradoERP', src.client_data.get('token_api'),
                                                        {
                                                            'cpf_cnpj': order.user.cpf if order.user.cpf is not None or order.user.cpf != '' else order.user.cnpj,
                                                            'codigo_cliente': client_erp_id
                                                        }):
                        logger.info(current_job + ' | Codigo Erp do cliente atualizado via api OkVendas')

    api_okvendas.put_protocol_orders(src.client_data.get('url_api') + '/pedido/integradoERP', src.client_data.get('token_api'), orders_to_protocol)


def insert_temp_order(order: Order, db_config: DatabaseConfig) -> bool:
    step = ''
    db = database.Connection(db_config)
    conn = db.get_conect()
    try:
        step = 'conexao'
        cursor = conn.cursor()

        # insere cliente
        step = 'insere cliente'

        cursor.execute(queries.get_insert_client_command(db_config.db_type), (
            order.user.name,
            order.user.company_name,
            order.user.cpf,
            order.user.cnpj,
            order.user.email,
            order.user.residential_phone,
            order.user.mobile_phone,
            order.user.address.zipcode,
            order.user.address.address_type,
            order.user.address.address_line,
            order.user.address.number,
            order.user.address.complement,
            order.user.address.neighbourhood,
            order.user.address.city,
            order.user.address.state,
            order.user.address.reference))

        if cursor.rowcount > 0:
            logger.info(current_job + f' | Cliente inserido para o pedido {order.order_id}')
            cursor.execute(queries.get_query_client(db_config.db_type), queries.get_command_parameter(db_config.db_type, [order.user.email]))
            client_id = cursor.fetchone()
            if client_id is None:
                cursor.close()
                raise Exception('Nao foi possivel obter o cliente inserido do banco de dados')
        else:
            cursor.close()
            raise Exception('O cliente nao foi inserido')

        # insere pedido
        step = 'insere pedido'
        cursor.execute(queries.get_insert_order_command(db_config.db_type), (
            order.order_id,
            order.order_code,
            order.date,
            order.status,
            client_id[0],
            order.total_amount,
            order.total_discount,
            order.freight_amount,
            order.additional_payment_amount,
            datetime.strptime(order.paid_date.replace('T', ' '), '%Y-%m-%d %H:%M:%S'),
            order.payment_type,
            order.flag,
            order.parcels,
            order.erp_payment_condition,
            order.tracking_code,
            datetime.strptime(order.delivery_forecast.replace('T', ' '), '%Y-%m-%d %H:%M:%S'),
            order.carrier,
            order.shipping_mode))

        if cursor.rowcount > 0:
            logger.info(current_job + f' | Pedido {order.order_id} inserido')
            cursor.execute(queries.get_query_order(db_config.db_type), order.order_id)
            order_id = cursor.fetchone()
            if order_id is None:
                cursor.close()
                raise Exception('Nao foi possivel obter o pedido inserido no banco de dados')
        else:
            cursor.close()
            raise Exception('O cliente nao foi inserido')

        # insere itens
        step = 'insere itens'
        for item in order.items:
            cursor.execute(queries.get_insert_order_items_command(db_config.db_type), (
                order.order_id,
                item.sku,
                item.erp_code,
                item.quantity,
                item.ean,
                item.value,
                item.discount,
                item.freight_value))

        cursor.close()
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(current_job + f' | Passo {step} - Erro durante a inserção dos dados do pedido {order.order_id}: {str(e)}', exc_info=True)
        conn.rollback()
        conn.close()
        return False


def call_order_procedures(db_config: DatabaseConfig, order_id: int) -> (bool, int, int):
    client_erp_id = 0
    order_erp_id = 0
    success = True
    db = database.Connection(db_config)
    conn = db.get_conect()
    try:
        cursor = conn.cursor()

        client_out_value = cursor.var(int)
        cursor.callproc('SP_PROCESSA_PEDIDO', [order_id, client_out_value])
        client_erp_id = client_out_value.getvalue()
        if client_erp_id is not None:
            logger.info(current_job + f' | Cliente ERP criado com sucesso {client_erp_id}')
            order_out_value = cursor.var(int)
            cursor.callproc('SP_PROCESSA_PEDIDO', [order_id, order_out_value])
            order_erp_id = order_out_value.getvalue()
            if order_erp_id is not None:
                logger.info(current_job + f' | Pedido ERP criado com sucesso {order_erp_id}')
            else:
                success = False
                logger.warning(current_job + f' | Nao foi possivel obter o id do pedido do ERP (retorno da procedure)')
        else:
            success = False
            logger.warning(current_job + f' | Nao foi possivel obter o id do cliente do ERP (retorno da procedure)')

        cursor.close()
        if success:
            conn.commit()
        else:
            conn.rollback()
        conn.close()
        return success, client_erp_id, order_erp_id
    except Exception as e:
        logger.error(current_job + f' | Erro: {e}', exc_info=True)
        conn.close()


def call_update_order_procedure(db_config: DatabaseConfig, order: Order) -> bool:
    success = True
    db = database.Connection(db_config)
    conn = db.get_conect()
    try:
        cursor = conn.cursor()
        order_updated = cursor.var(int)
        cursor.callproc('SP_ATUALIZA_PEDIDO', [order.order_id, order.status, order_updated])
        updated = order_updated.getvalue()
        if updated is not None and updated > 0:
            logger.info(current_job + f' | Pedido atualizado com sucesso {order.order_id}')
        else:
            success = False
            logger.warning(current_job + f' | Nao foi possivel o pedido informado {order.order_id}')

        cursor.close()
        if success:
            conn.commit()
        else:
            conn.rollback()
        conn.close()
        return success
    except Exception as e:
        logger.error(current_job + f' | Erro: {e}', exc_info=True)
        conn.close()
