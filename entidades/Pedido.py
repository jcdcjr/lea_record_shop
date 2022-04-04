import uuid

from validacoes.Validacao import validar_pedido
from entidades.Cliente import Cliente
from entidades.Disco import Disco
from datetime import datetime


class Pedido:
    tabela = 'LeaRecordShop'

    def __init__(self, documento, disco_id, quantidade):
        erro_validacao = validar_pedido(documento, disco_id, quantidade)

        if erro_validacao:
            raise erro_validacao

        self.cliente = None
        self.disco = None
        self.documento = str(documento)
        self.disco_id = str(disco_id)
        self.quantidade = int(quantidade)
        self.data_hora = datetime.now()

    def cadastrar(self, dynamodb):
        try:
            cliente = Cliente(self.documento)
            ret_cliente = cliente.obter_por_id(dynamodb)

            if ret_cliente.__contains__('Erro:'):
                return ret_cliente

            self.cliente = ret_cliente

            disco = Disco()
            ret_disco = disco.obter_por_id(self.disco_id, dynamodb)

            if ret_disco.__contains__('Erro:'):
                return ret_disco

            self.disco = ret_disco
            self.data_hora = datetime.now()
            table = dynamodb.Table(self.tabela)
            response = table.put_item(
                Item={
                    'pk': 'PEDIDOS#' + str(uuid.uuid1()),
                    'sk': 'PEDIDO',
                    'data': str(self.data_hora),
                    'cliente': self.cliente,
                    'disco': self.disco,
                    'quantidade': self.quantidade
                }
            )
            return response
        except Exception:
            raise
