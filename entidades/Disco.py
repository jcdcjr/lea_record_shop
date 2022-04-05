from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import uuid
from validacoes.Validacao import validar_disco, validar_disco_id, validar_quantidade


class Disco:
    tabela = 'LeaRecordShop'

    def __init__(self):
        self.disco_id = None
        self.nome = None
        self.artista = None
        self.ano_lancamento = None
        self.estilo = None
        self.quantidade = None

    def __atualizar_estoque(self, table):
        return table.update_item(
            Key={
                'pk': 'DISCOS#' + str(self.disco_id),
                'sk': 'DISCO'
            },
            UpdateExpression="set quantidade=:q, nome=:n, artista=:a, ano_lancamento=:al, estilo=:e",
            ExpressionAttributeValues={
                ':q': self.quantidade,
                ':n': self.nome,
                ':a': self.artista,
                ':al': self.ano_lancamento,
                ':e': self.estilo
            },
            ReturnValues="UPDATED_NEW"
        )

    def __atualizar_dados(self, table):
        return table.update_item(
            Key={
                'pk': 'DISCOS#' + str(self.disco_id),
                'sk': 'DISCO'
            },
            ExpressionAttributeNames={
                '#data': 'data'
            },
            UpdateExpression="set #data=:d, nome=:n, artista=:a, ano_lancamento=:al, estilo=:e, quantidade=:q",
            ExpressionAttributeValues={
                ':n': self.nome,
                ':a': self.artista,
                ':al': self.ano_lancamento,
                ':e': self.estilo,
                ':d': self.nome + '#' + self.artista + '#' + str(self.ano_lancamento) + '#' + self.estilo + '#',
                ':q': self.quantidade
            },
            ReturnValues="UPDATED_NEW"
        )

    def __extrair_item(self, quantidade_estoque):
        self.quantidade = quantidade_estoque - self.quantidade

    def __inserir(self, table):
        return table.put_item(
            Item={
                'pk': 'DISCOS#' + str(uuid.uuid1()),
                'sk': 'DISCO',
                'data': self.nome + '#' + self.artista + '#' + str(self.ano_lancamento) + '#' + self.estilo + '#',
                'nome': self.nome,
                'artista': self.artista,
                'ano_lancamento': self.ano_lancamento,
                'estilo': self.estilo,
                'quantidade': 0
            }
        )

    def __montar_disco(self, nome, artista, ano_lancamento, estilo):
        self.nome = str(nome)
        self.artista = str(artista)
        self.ano_lancamento = str(ano_lancamento)
        self.estilo = str(estilo)

    def __obter_item(self, table):
        return table.get_item(
            Key={
                'pk': 'DISCOS#' + str(self.disco_id),
                'sk': 'DISCO'
            }
        )

    def __remover_disco(self, table):
        return table.delete_item(
            Key={
                'pk': 'DISCOS#' + str(self.disco_id),
                'sk': 'DISCO'
            }
        )

    def __validacao_disco_id(self, disco_id):
        if not disco_id:
            return 'Erro: Código do disco é obrigatório!'

        validacao_disco_id = validar_disco_id(disco_id)

        if not validacao_disco_id:
            return 'Erro: Código do disco é inválido!'

        self.disco_id = disco_id
        return None

    def __validacao_dados_disco(self, disco_id, nome, artista, ano_lancamento, estilo):
        erro_validacao_disco_id = self.__validacao_disco_id(disco_id)

        if erro_validacao_disco_id:
            return erro_validacao_disco_id

        erro_validacao = validar_disco(nome, artista, ano_lancamento, estilo)

        if erro_validacao:
            return erro_validacao
        else:
            self.__montar_disco(nome, artista, ano_lancamento, estilo)
            return None

    def __validacao_estoque(self, disco_id, quantidade):
        erro_validacao_disco_id = self.__validacao_disco_id(disco_id)

        if erro_validacao_disco_id:
            return erro_validacao_disco_id

        erro_validacao_quantidade = self.__validacao_quantidade(quantidade)

        if erro_validacao_quantidade:
            return erro_validacao_quantidade

        self.disco_id = disco_id
        self.quantidade = int(quantidade)

        return None

    def __validacao_quantidade(self, quantidade):
        if not quantidade:
            return 'Erro: Quantidade é obrigatória!'

        validacao_quantidade = validar_quantidade(quantidade)

        if not validacao_quantidade:
            return 'Erro: Quantidade inválida!'

        return None

    def atualizar_dados_disco(self, disco_id, nome, artista, ano_lancamento, estilo, dynamodb):
        try:
            validacao_dados_disco = self.__validacao_dados_disco(disco_id, nome, artista, ano_lancamento, estilo)

            if validacao_dados_disco:
                return validacao_dados_disco

            table = dynamodb.Table(self.tabela)

            disco = self.obter_por_id(self.disco_id, dynamodb)
            if disco.__contains__('Erro:'):
                return disco

            self.quantidade = int(disco['quantidade'])

            response = self.__atualizar_dados(table)

            return response
        except Exception as e:
            raise 'Erro: Falha ao atualizar os dados do disco. Motivo: ' + e

    def cadastrar(self, nome, artista, ano_lancamento, estilo, dynamodb):
        erro_validacao = validar_disco(nome, artista, ano_lancamento, estilo)

        if erro_validacao:
            return erro_validacao

        self.__montar_disco(nome, artista, ano_lancamento, estilo)

        try:
            table = dynamodb.Table(self.tabela)
            response = self.__inserir(table)
            return response
        except Exception as e:
            raise 'Erro: Falha ao cadastrar o disco. Motivo:' + e

    def listar_discos(self, dynamodb, nome=None, artista=None, ano_lancamento=None, estilo=None):

        table = dynamodb.Table(self.tabela)

        try:
            if not nome and not artista and not ano_lancamento and not estilo:
                response = table.query(
                    IndexName='gsi_1',
                    KeyConditionExpression=Key('sk').eq('DISCO'))
            else:
                response = table.query(
                    IndexName='gsi_1',
                    KeyConditionExpression=Key('sk').eq('DISCO'),
                    FilterExpression=Attr('nome').contains(nome) | Attr('artista').contains(artista) |
                                     Attr('ano_lancamento').contains(ano_lancamento) | Attr('estilo').contains(estilo)
                )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise 'Erro: Foi encontrado um erro inesperado!'
        else:
            return response['Items']

    def obter_por_id(self, disco_id, dynamodb):
        erro_validacao = self.__validacao_disco_id(disco_id)

        if erro_validacao:
            return erro_validacao

        self.disco_id = str(disco_id)

        try:
            table = dynamodb.Table(self.tabela)

            response = self.__obter_item(table)

            if not response.__contains__('Item'):
                return 'Erro: Disco nao localizado'

            return response['Item']
        except Exception as e:
            raise 'Erro: Falha ao obter o disco. Motivo: ' + e

    def realizar_baixa_estoque(self, disco_id, quantidade, dynamodb):
        try:
            erro_validacao_estoque = self.__validacao_estoque(disco_id, quantidade)

            if erro_validacao_estoque:
                return erro_validacao_estoque

            disco = self.obter_por_id(self.disco_id, dynamodb)
            if disco.__contains__('Erro:'):
                return disco

            self.__montar_disco(disco['nome'], disco['artista'], disco['ano_lancamento'], disco['estilo'])

            quantidade_atual = int(disco['quantidade'])

            if quantidade_atual < self.quantidade:
                return 'Erro: Quantidade indisponível no momento'

            self.__extrair_item(quantidade_atual)

            table = dynamodb.Table(self.tabela)

            response = self.__atualizar_estoque(table)

            return response
        except Exception as e:
            raise 'Erro: Falha ao repor estoque. Motivo:' + e

    def remover(self, disco_id, dynamodb):
        try:
            erro_validacao = self.__validacao_disco_id(disco_id)

            if erro_validacao:
                return erro_validacao

            table = dynamodb.Table(self.tabela)

            disco = self.obter_por_id(self.disco_id, dynamodb)
            if disco.__contains__('Erro:'):
                return disco

            response = self.__remover_disco(table)

            return response
        except Exception as e:
            raise 'Erro: Falha ao remover o disco. Motivo: ' + e

    def repor_estoque_disco(self, disco_id, quantidade, dynamodb):
        try:
            erro_validacao = self.__validacao_estoque(disco_id, quantidade)

            if erro_validacao:
                return erro_validacao

            disco = self.obter_por_id(self.disco_id, dynamodb)
            if disco.__contains__('Erro:'):
                return disco

            self.__montar_disco(disco['nome'], disco['artista'], disco['ano_lancamento'], disco['estilo'])

            self.quantidade += int(disco['quantidade'])

            table = dynamodb.Table(self.tabela)

            response = self.__atualizar_estoque(table)
            return response
        except Exception as e:
            raise 'Erro: Falha ao repor estoque. Motivo:' + e
