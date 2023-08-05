import logging
import src.database.connection as database
from src.database.utils import DatabaseConfig
import src.api.okvendas as api_okvendas
from src.services import slack
from src.database import queries
import src

logger = logging.getLogger()


def job_insert_stock_semaphore(job_config_dict: dict):
    db_config = DatabaseConfig(**job_config_dict)
    if db_config.sql is None:
        logger.warning(job_config_dict.get('job') + ' | Comando sql para criar produtos nao encontrado')
    else:
        conexao = database.Connection(db_config)
        conn = conexao.get_conect()
        cursor = conn.cursor()

        try:
            cursor.execute(db_config.sql)
            cursor.close()
            conn.commit()
        except Exception as ex:
            slack.registerErro("Erro executando: {}".format(db_config.sql))
            logger.error(str(ex), exc_info=True)

        conn.close()


def job_send_stocks(job_config_dict: dict):
    estoque_por_unidade = True
    # if 'UnidadeDistribuicao' not in globals.url_estoque:
    #     estoque_por_unidade = False
    db_config = DatabaseConfig(**job_config_dict)
    stocks = query_stocks(db_config, estoque_por_unidade)
    p_size = len(stocks) if stocks is not None else 0

    if p_size > 0:
        logger.debug("Total de produtos atualiza estoque API: {}".format(p_size))
        jsn_prods = api_okvendas.send_stocks(src.client_data.get('url_api') + '/catalogo/estoqueUnidadeDistribuicao', stocks, src.client_data.get('token_api'))

        atualizados = []
        mensagens = []

        if jsn_prods is not None:
            logger.debug('Atualizando produtos no semaforo')
            conexao = database.Connection(db_config)
            conn = conexao.get_conect()
            cursor = conn.cursor()

            # Identifiers, Status, Message, Protocolo
            for p in jsn_prods:
                if p['Status'] == 1:
                    cod_erp = p['Identifiers'][0]  # ???
                    try:
                        sql_protocolar_estoque = queries.get_stock_protocol_command(db_config.db_type)
                        cursor.execute(sql_protocolar_estoque, queries.get_command_parameter(db_config.db_type, [cod_erp]))
                        atualizados.append(cod_erp)
                    except Exception as ex:
                        logger.error(str(ex), exc_info=True)
                else:
                    mensagens.append(p['Message'])

            cursor.close()
            conn.commit()
            conn.close()

            total = len(atualizados)
            logger.debug('Atualizado produtos no semaforo: {}'.format(total))
    else:
        logger.warning("Nao ha produtos para atualizar estoque")


def query_stocks(db_config: DatabaseConfig, stock_ud: bool):
    produtos = None
    if db_config.sql is None:
        slack.registerWarn("Query estoque de produtos nao configurada!")
    else:
        try:
            conexao = database.Connection(db_config)
            conn = conexao.get_conect()
            cursor = conn.cursor()

            # print(db_config.sql)
            cursor.execute(db_config.sql)
            rows = cursor.fetchall()
            # print(rows)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()
            if len(results) > 0:
                if stock_ud:
                    produtos = stock_ud_dict(results)
                else:
                    produtos = stock_dict(results)

        except Exception as ex:
            logger.error(str(ex), exc_info=True)

    return produtos


def stock_dict(produtos):
    lista = []
    for row in produtos:
        pdict = {
            'codigo_erp': row[1],
            'quantidade': int(row[2])
        }
        lista.append(pdict)

    return lista


def stock_ud_dict(produtos):
    lista = []
    for row in produtos:
        pdict = {
            'unidade_distribuicao': row[0],
            'codigo_erp': row[1],
            'quantidade_total': int(row[2]),
            'parceiro': 1
        }
        lista.append(pdict)

    return lista