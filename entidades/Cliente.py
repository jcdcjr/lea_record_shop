from botocore.exceptions import ClientError
from datetime import datetime
from validacoes.Validacao import validar_cliente, validar_documento


class Cliente:
    tabela = 'LeaRecordShop'

    def __init__(self, documento):
        self.__validar_documento(documento)
        self.documento = str(documento)
        self.nome_completo = None
        self.data_nascimento = None
        self.email = None
        self.telefone = None

    def __alterar_status(self, table):
        return table.update_item(
            Key={
                'pk': 'CLIENTES#' + self.documento,
                'sk': 'CLIENTE'
            },
            ExpressionAttributeNames={
                "#data": "data"
            },
            UpdateExpression="set #data=:d",
            ExpressionAttributeValues={
                ':d': str(0)
            },
            ReturnValues="UPDATED_NEW"
        )

    def __atualizar_dados(self, table):
        return table.update_item(
            Key={
                'pk': 'CLIENTES#' + self.documento,
                'sk': 'CLIENTE'
            },
            UpdateExpression="set nome_completo=:nc, data_nascimento=:dn, email=:e, telefone=:t",
            ExpressionAttributeValues={
                ':nc': self.nome_completo,
                ':dn': str(self.data_nascimento),
                ':e': self.email,
                ':t': self.telefone
            },
            ReturnValues="UPDATED_NEW"
        )

    def __inserir(self, table):
        return table.put_item(
            Item={
                'pk': 'CLIENTES#' + self.documento,
                'sk': 'CLIENTE',
                'data': str(1),
                'documento': self.documento,
                'nome_completo': self.nome_completo,
                'data_nascimento': str(self.data_nascimento),
                'email': self.email,
                'telefone': self.telefone
            }
        )

    def __montar_cliente(self, data_nascimento, email, nome_completo, telefone):
        self.nome_completo = str(nome_completo)
        self.data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d')
        self.email = str(email)
        self.telefone = str(telefone)

    def __obter_cliente(self, table):
        return table.get_item(
            Key={
                'pk': 'CLIENTES#' + str(self.documento),
                'sk': 'CLIENTE'
            }
        )

    @staticmethod
    def __validar_documento(documento):
        if not documento:
            return 'Documento é obrigatório!'

        if not validar_documento(documento):
            return 'Documento invalido!'

    def atualizar(self, nome_completo, data_nascimento, email, telefone, dynamodb):
        try:
            erro_validacao = validar_cliente(nome_completo, data_nascimento, email, telefone)

            if erro_validacao:
                return erro_validacao
            else:
                self.__montar_cliente(data_nascimento, email, nome_completo, telefone)

            table = dynamodb.Table(self.tabela)

            cliente = self.obter_por_id(dynamodb)
            if cliente.__contains__('Erro:'):
                return cliente

            if cliente['data'] == '0':
                return 'Erro: Não é possível atualizar os dados cadastrais. Motivo: Cliente inativo'

            response = self.__atualizar_dados(table)
        except Exception as e:
            raise e
        else:
            return response

    def cadastrar(self, nome_completo, data_nascimento, email, telefone, dynamodb):
        try:
            erro_validacao = validar_cliente(nome_completo, data_nascimento, email, telefone)

            if erro_validacao:
                raise erro_validacao

            self.__montar_cliente(data_nascimento, email, nome_completo, telefone)

            table = dynamodb.Table(self.tabela)
            response = self.__inserir(table)
        except Exception as e:
            raise e
        else:
            return response

    def inativar(self, dynamodb):
        try:
            table = dynamodb.Table(self.tabela)

            response = self.__alterar_status(table)
        except Exception as e:
            raise e
        else:
            return response

    def obter_por_id(self, dynamodb):
        try:
            table = dynamodb.Table(self.tabela)

            response = self.__obter_cliente(table)

            if not response.__contains__('Item'):
                return 'Erro: Cliente nao localizado'
        except ClientError as e:
            raise e.response['Error']['Message']
        else:
            return response['Item']
