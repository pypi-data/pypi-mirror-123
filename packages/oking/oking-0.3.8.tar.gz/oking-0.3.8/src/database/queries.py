

def get_product_protocol_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return 'update openk_semaforo.produto set data_sincronizacao = now() where codigo_erp = %s and codigo_erp_sku = %s'
	elif connection_type.lower() == 'oracle':
		return 'update openk_semaforo.produto set data_sincronizacao = TRUNC(SYSDATE) where codigo_erp = :codigo_erp and codigo_erp_sku = :codigo_erp_sku'
	elif connection_type.lower() == 'sqlserver':
		return 'update openk_semaforo.produto set data_sincronizacao = now() where codigo_erp = %s and codigo_erp_sku = %s'


def get_stock_protocol_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return 'update openk_semaforo.estoque_produto set data_sincronizacao = now() where codigo_erp = %s'
	elif connection_type.lower() == 'oracle':
		return 'update openk_semaforo.estoque_produto set data_sincronizacao = current_date where codigo_erp = :codigo_erp'
	elif connection_type.lower() == 'sqlserver':
		return 'update openk_semaforo.estoque_produto set data_sincronizacao = now() where codigo_erp = %s'


def get_price_protocol_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return 'update openk_semaforo.preco_produto set data_sincronizacao = now() where codigo_erp = %s'
	elif connection_type.lower() == 'oracle':
		return 'update openk_semaforo.preco_produto set data_sincronizacao = current_date where codigo_erp = :codigo_erp'
	elif connection_type.lower() == 'sqlserver':
		return 'update openk_semaforo.preco_produto set data_sincronizacao = now() where codigo_erp = %s'


def get_insert_client_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return ''
	elif connection_type.lower() == 'oracle':
		return '''INSERT INTO OPENK_SEMAFORO.CLIENTE (NOME, RAZAO_SOCIAL, CPF, CNPJ, EMAIL, TELEFONE_RESIDENCIAL, TELEFONE_CELULAR, CEP, 
														TIPO_LOGRADOURO, LOGRADOURO,NUMERO, COMPLEMENTO, BAIRRO, CIDADE, ESTADO, REFERENCIA) 
				VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16) '''
	elif connection_type.lower() == 'sqlserver':
		return ''


def get_insert_order_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return ''
	elif connection_type.lower() == 'oracle':
		return '''INSERT INTO OPENK_SEMAFORO.PEDIDO (PEDIDO_ID, PEDIDO_VENDA_ID, DATA_PEDIDO, STATUS, CLIENTE_ID, VALOR, VALOR_DESCONTO, VALOR_FRETE, 
					VALOR_ADICIONAL_FORMA_PAGAMENTO, DATA_PAGAMENTO, TIPO_PAGAMENTO, BANDEIRA, PARCELAS, CONDICAO_PAGAMENTO_ERP, CODIGO_RASTREIO, DATA_PREVISAO_ENTREGA, 
					TRANSPORTADORA, MODO_ENVIO)
					VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18) '''
	elif connection_type.lower() == 'sqlserver':
		return ''


def get_insert_order_items_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return ''
	elif connection_type.lower() == 'oracle':
		return '''INSERT INTO OPENK_SEMAFORO.ITENS_PEDIDO (PEDIDO_ID, SKU, CODIGO_ERP, QUANTIDADE, EAN, VALOR, VALOR_DESCONTO, VALOR_FRETE)
					VALUES (:1, :2, :3, :4, :5, :6, :7, :8)'''
	elif connection_type.lower() == 'sqlserver':
		return ''


def get_query_client(connection_type: str):
	if connection_type.lower() == 'mysql':
		return ''
	elif connection_type.lower() == 'oracle':
		return 'SELECT ID FROM OPENK_SEMAFORO.CLIENTE WHERE EMAIL = :email'
	elif connection_type.lower() == 'sqlserver':
		return ''


def get_query_order(connection_type: str):
	if connection_type.lower() == 'mysql':
		return ''
	elif connection_type.lower() == 'oracle':
		return 'SELECT ID FROM OPENK_SEMAFORO.PEDIDO WHERE PEDIDO_ID = :id'
	elif connection_type.lower() == 'sqlserver':
		return ''


def get_command_parameter(connection_type: str, parameters: list):
	if connection_type.lower() == 'mysql':
		return tuple(parameters)
	elif connection_type.lower() == 'oracle':
		return parameters
	elif connection_type.lower() == 'sqlserver':
		return parameters
