import json
import logging
import jsonpickle
import src
from src.services import srequest
import requests
from src.services import slack

logger = logging.getLogger()


class CatalogoResponse:
    def __init__(self, Status: int, Message: str, codigo_erp: str = '', protocolo: str = '', loja: str = '') -> None:
        self.codigo_erp = codigo_erp
        self.status = Status
        self.message = Message
        self.protocolo = protocolo
        self.loja = loja


def obj_dict(obj):
    return obj.__dict__


def object_list_to_dict(obj_list: list):
    lista = []
    for obj in obj_list:
        lista.append(obj.toJSON())
    return lista


def post_produtos(produtos: list):
    try:
        url = f'{src.client_data.get("url_api")}/catalogo/produtos'

        json_produtos = jsonpickle.encode(produtos, unpicklable=False)
        logger.info(f'Enviando produto para api okvendas {json_produtos}')
        response = requests.post(url, json=json.loads(json_produtos), headers={
            'Content-type': 'application/json',
            'Accept': 'text/html',
            'access-token': src.client_data.get('token_api')})

        obj = jsonpickle.decode(response.content)
        result = []
        if 200 <= response.status_code <= 299:
            for res in obj:
                result.append(CatalogoResponse(**res))
        else:
            if type(obj) is list:
                for res in obj:
                    result.append(CatalogoResponse(**res))
            else:
                result.append(CatalogoResponse(**obj))

        return result
    except Exception as e:
        logger.error(f'Erro ao enviar produto para api okvendas {e}', exc_info=True)


def send_stocks(url, body, token):
    logger.debug("POST: {}".format(url))
    try:
        # auth = HTTPBasicAuth('teste@example.com', 'real_password')
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/html',
                   'access-token': token}

        response = requests.post(url, json=body, headers=headers)

        if response.status_code >= 200 and response.status_code <= 299:
            return response.json(), response.status_code
        else:
            slack.registerErro('Retorno sem sucesso - status ' +
                               str(response.status_code) + ' ' + response.text)
            if response.content is not None and response.content != '':
                return response.json(), response.status_code

    except Exception as ex:
        logger.error(str(ex), exc_info=True)
        return None, response.status_code
