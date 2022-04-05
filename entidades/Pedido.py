from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from datetime import datetime
from entidades.Cliente import Cliente
from entidades.Disco import Disco
import uuid
from validacoes.Validacao import validar_documento, validar_data_hora_pedido, validar_pedido


class Pedido:
    tabela = 'LeaRecordShop'

    def __init__(self):
        self.data_hora = datetime.now()
        self.documento = None
        self.disco_id = None
        self.quantidade = None
        self.cliente = None
        self.disco = None

    def __inserir(self, table):
        return table.put_item(
            Item={
                'pk': 'PEDIDOS#' + str(uuid.uuid1()),
                'sk': 'PEDIDO',
                'data': str(self.data_hora),
                'cliente': self.cliente,
                'disco': self.disco,
                'quantidade': self.quantidade
            }
        )

    def __monta_pedido(self, documento, disco_id, quantidade):
        self.documento = str(documento)
        self.disco_id = str(disco_id)
        self.quantidade = int(quantidade)

    def __validar_obtencao_cliente(self, dynamodb):
        cliente = Cliente(self.documento)
        ret_cliente = cliente.obter_por_id(dynamodb)

        if ret_cliente.__contains__('Erro:'):
            return ret_cliente

        self.cliente = ret_cliente

        return None

    def __validar_obtencao_disco(self, dynamodb):
        disco = Disco()
        ret_disco = disco.obter_por_id(self.disco_id, dynamodb)

        if ret_disco.__contains__('Erro:'):
            return ret_disco

        self.disco = ret_disco

        return None

    @staticmethod
    def __validar_datas(data_inicio, data_fim):
        if data_inicio:
            if not validar_data_hora_pedido(data_inicio):
                raise 'Data início inválida!'

        if data_fim:
            if not validar_data_hora_pedido(data_fim):
                raise 'Data Fim inválida!'

    @staticmethod
    def __validar_documento(documento):
        if documento:
            if not validar_documento(documento):
                raise 'Documento inválido!'

    @staticmethod
    def __validar_parametros(documento, disco_id, quantidade):
        erro_validacao = validar_pedido(documento, disco_id, quantidade)

        if erro_validacao:
            raise erro_validacao

    def cadastrar(self, documento, disco_id, quantidade, dynamodb):
        try:
            self.__validar_parametros(documento, disco_id, quantidade)

            erro_obtencao_cliente = self.__validar_obtencao_cliente(dynamodb)

            if erro_obtencao_cliente:
                raise erro_obtencao_cliente

            erro_obtencao_disco = self.__validar_obtencao_disco(dynamodb)

            if erro_obtencao_disco:
                raise erro_obtencao_disco

            disco = Disco()
            baixa_estoque = disco.realizar_baixa_estoque(self.disco_id, self.quantidade, dynamodb)

            if baixa_estoque.__contains__('Erro:'):
                return baixa_estoque

            table = dynamodb.Table(self.tabela)

            response = self.__inserir(table)
        except Exception as e:
            raise e
        else:
            return response

    def listar_pedidos(self, documento, data_inicio, data_fim, dynamodb):
        try:
            table = dynamodb.Table(self.tabela)
            if documento and not data_inicio and not data_fim:
                self.__validar_documento(documento)
                response = table.query(
                    IndexName='gsi_1',
                    KeyConditionExpression=Key('sk').eq('PEDIDO'),
                    FilterExpression=Attr('cliente.documento').eq(documento)
                )
            elif documento and data_inicio and data_fim:
                self.__validar_documento(documento)
                self.__validar_datas(data_inicio, data_fim)
                response = table.query(
                    IndexName='gsi_1',
                    KeyConditionExpression=Key('sk').eq('PEDIDO') & Key('data').between(data_inicio, data_fim),
                    FilterExpression=Attr('cliente.documento').eq(documento)
                )
            elif documento and data_inicio and not data_fim:
                self.__validar_documento(documento)
                self.__validar_datas(data_inicio, data_fim)
                response = table.query(
                    IndexName='gsi_1',
                    KeyConditionExpression=Key('sk').eq('PEDIDO') & Key('data').gte(data_inicio),
                    FilterExpression=Attr('cliente.documento').eq(documento)
                )
            elif documento and not data_inicio and data_fim:
                self.__validar_documento(documento)
                self.__validar_datas(data_inicio, data_fim)
                response = table.query(
                    IndexName='gsi_1',
                    KeyConditionExpression=Key('sk').eq('PEDIDO') & Key('data').lte(data_fim),
                    FilterExpression=Attr('cliente.documento').eq(documento)
                )
            elif not documento and not data_inicio and data_fim:
                self.__validar_datas(data_inicio, data_fim)
                response = table.query(
                    IndexName='gsi_1',
                    KeyConditionExpression=Key('sk').eq('PEDIDO') & Key('data').lte(data_fim)
                )
            elif not documento and data_inicio and not data_fim:
                self.__validar_datas(data_inicio, data_fim)
                response = table.query(
                    IndexName='gsi_1',
                    KeyConditionExpression=Key('sk').eq('PEDIDO') & Key('data').gte(data_inicio)
                )
            elif not documento and data_inicio and data_fim:
                self.__validar_documento(documento)
                self.__validar_datas(data_inicio, data_fim)
                response = table.query(
                    IndexName='gsi_1',
                    KeyConditionExpression=Key('sk').eq('PEDIDO') & Key('data').between(data_inicio, data_fim)
                )
            else:
                response = table.query(
                    IndexName='gsi_1',
                    KeyConditionExpression=Key('sk').eq('PEDIDO')
                )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            return response['Items']
