import logging
from datetime import datetime
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

    for q_order in queue:
        order = api_okvendas.get_order(
            url=src.client_data.get('url_api') + '/pedido/{0}',
            token=src.client_data.get('token_api'),
            order_id=q_order.pedido_id)

        if order.codigo_referencia is not None and order.codigo_referencia != '':
            # atualiza status do pedido no banco de dados
            update_tmp_order(order)
        else:
            # insere pedido no banco de dados
            inserted = insert_temp_order(order, db_config)
            if inserted:
                call_order_procedures(db_config)


def insert_temp_order(order: Pedido, db_config: DatabaseConfig) -> bool:
    step = ''
    db = database.Connection(db_config)
    conn = db.get_conect()
    try:
        step = 'conexao'
        cursor = conn.cursor()

        # insere cliente
        step = 'insere cliente'
        cursor.execute(queries.get_insert_client_command(db_config.db_type), queries.get_command_parameter(db_config.db_type, [
            order.usuario.nome,
            order.usuario.cpf,
            order.usuario.cnpj,
            order.usuario.email,
            order.usuario.TelefoneResidencial,
            order.usuario.TelefoneCelular,
            order.usuario.Endereco.cep,
            order.usuario.Endereco.tipo_logradouro,
            order.usuario.Endereco.logradouro,
            order.usuario.Endereco.numero,
            order.usuario.Endereco.complemento,
            order.usuario.Endereco.bairro,
            order.usuario.Endereco.cidade,
            order.usuario.Endereco.estado,
            order.usuario.Endereco.pais,
            order.usuario.Endereco.referencia]))

        if cursor.rowcount > 0:
            logger.info(current_job + f' | Cliente inserido para o pedido {order.id}')
            cursor.execute(queries.get_query_client(db_config.db_type), order.usuario.email)
            client_id = cursor.fetchone()
            if client_id is None:
                cursor.close()
                raise Exception('Nao foi possivel obter o cliente inserido do banco de dados')
        else:
            cursor.close()
            raise Exception('O cliente nao foi inserido')

        # insere pedido
        step = 'insere pedido'
        data_pago = datetime.now()
        cursor.execute(queries.get_insert_order_command(db_config.db_type), queries.get_command_parameter(db_config.db_type, [
            order.id,
            order.pedido_venda_id,
            order.data_pedido,
            order.status,
            client_id,
            order.valor_total,
            order.valor_desconto,
            order.valor_frete,
            order.valor_adicional_forma_pagamento,
            data_pago if order.status.endswith('confirmado.') else None,
            order.pagamento[0].opcao_pagamento,
            order.pagamento[0].bandeira,
            order.pagamento[0].parcelas,
            order.pagamento[0].condicao_pagamento_erp,
            order.codigo_rastreio,
            order.previsao_entrega,
            order.transportadora,
            order.forma_envio_parceiro[0].modo_envio]))

        if cursor.rowcount > 0:
            logger.info(current_job + f' | Pedido {order.id} inserido')
            cursor.execute(queries.get_query_order(db_config.db_type), order.id)
            order_id = cursor.fetchone()
            if order_id is None:
                cursor.close()
                raise Exception('Nao foi possivel obter o pedido inserido no banco de dados')
        else:
            cursor.close()
            raise Exception('O cliente nao foi inserido')

        # insere itens
        step = 'insere itens'
        for item in order.itens:
            cursor.execute(queries.get_insert_order_items_command(db_config.db_type), queries.get_command_parameter(db_config.db_type, [
                order.id,
                item.sku,
                item.erp_code,
                item.quantity,
                item.ean,
                item.value,
                item.discount,
                item.freight_value]))

        cursor.close()
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(current_job + f' | Passo {step} - Erro durante a inserção dos dados do pedido {order.id}: {str(e)}', exc_info=True)
        conn.rollback()
        conn.close()
        return False


def update_tmp_order(order: Pedido) -> bool:
    return True


def call_order_procedures(db_config: DatabaseConfig, order_id: int) -> bool:
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
                logger.warning(current_job + f' | Nao foi possivel obter o id do pedido do ERP (retorno da procedure)')
        else:
            logger.warning(current_job + f' | Nao foi possivel obter o id do cliente do ERP (retorno da procedure)')

        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(current_job + f' | Erro: {e}', exc_info=True)
        conn.close()
