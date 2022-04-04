import uuid
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
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

    def atualizar_dados_disco(self, disco_id, nome, artista, ano_lancamento, estilo, dynamodb):
        try:
            erro_validacao = validar_disco(nome, artista, ano_lancamento, estilo)

            if erro_validacao:
                return erro_validacao
            else:
                self.montar_disco(nome, artista, ano_lancamento, estilo)

            if not disco_id(disco_id):
                return 'Código do disco ´obrigatório!'

            if not validar_disco_id(disco_id):
                return 'Código do disco inválido!'

            self.disco_id = str(disco_id)

            table = dynamodb.Table(self.tabela)

            disco = self.obter_por_id(self.disco_id, dynamodb)
            if disco.__contains__('Erro:'):
                return disco

            response = table.update_item(
                Key={
                    'pk': 'DISCOS#' + str(self.disco_id),
                    'sk': 'DISCO'
                },
                UpdateExpression="set nome=:n, artista=:a, ano_lancamento=:al, estilo=:e",
                ExpressionAttributeValues={
                    ':n': self.nome,
                    ':a': self.artista,
                    ':al': self.ano_lancamento,
                    ':e': self.estilo
                },
                ReturnValues="UPDATED_NEW"
            )
            return response

        except Exception as ex:
            raise ex

    def cadastrar(self, nome, artista, ano_lancamento, estilo, dynamodb):
        erro_validacao = validar_disco(nome, artista, ano_lancamento, estilo)

        if erro_validacao:
            return erro_validacao
        else:
            self.montar_disco(nome, artista, ano_lancamento, estilo)
        try:
            table = dynamodb.Table(self.tabela)
            response = table.put_item(
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
            return response
        except Exception as ex:
            raise ex

    @staticmethod
    def filtrar(ano_lancamento, artista, estilo, nome):
        filtro = ''

        if nome:
            filtro += str(nome) + '#'
        else:
            filtro += 'NULL#'

        if artista:
            filtro += str(artista) + '#'
        else:
            filtro += 'NULL#'

        if ano_lancamento:
            filtro += str(ano_lancamento) + '#'
        else:
            filtro += 'NULL#'

        if estilo:
            filtro += str(estilo) + '#'
        else:
            filtro += 'NULL#'

        return filtro

    def listar_discos(self, nome, artista, ano_lancamento, estilo, dynamodb):
        filtro = self.filtrar(ano_lancamento, artista, estilo, nome)

        table = dynamodb.Table(self.tabela)

        try:
            response = table.query(
                IndexName='gsi_1',
                KeyConditionExpression=Key('sk').eq('DISCO'),
                FilterExpression="contains(#data, :data)",
                ExpressionAttributesNames={'#data', 'data'},
                ExpressionAttributesValues={":data": filtro})

        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            return response['Items']

    def montar_disco(self, nome, artista, ano_lancamento, estilo):
        self.nome = str(nome)
        self.artista = str(artista)
        self.ano_lancamento = int(ano_lancamento)
        self.estilo = str(estilo)

    def obter_por_id(self, disco_id, dynamodb):
        if not disco_id:
            return 'Erro: Código disco obrigatório!'
        if not validar_disco_id(disco_id):
            return 'Erro: Código disco inválido!'

        self.disco_id = str(disco_id)

        try:
            table = dynamodb.Table(self.tabela)

            response = table.get_item(
                Key={
                    'pk': 'DISCOS#' + str(self.disco_id),
                    'sk': 'DISCO'
                }
            )
            if not response.__contains__('Item'):
                return 'Erro: Disco nao localizado'

            return response['Item']
        except Exception as ex:
            raise ex

    def realizar_baixa_estoque(self, disco_id, quantidade, dynamodb):
        try:
            if not disco_id:
                return 'Código do disco é obrigatório!'

            if not validar_disco_id(disco_id):
                return 'Código do disco inválido!'

            if not quantidade:
                return 'Quantidade ´é obrigatória!'

            if not validar_quantidade(quantidade):
                return 'Quantidade inválida!'

            self.disco_id = disco_id
            self.quantidade = int(quantidade)

            table = dynamodb.Table(self.tabela)

            response = table.update_item(
                Key={
                    'pk': 'DISCOS#' + str(self.disco_id),
                    'sk': 'DISCO'
                },
                UpdateExpression="set nome=:n, artista=:a, ano_lancamento=:al, estilo=:e",
                ExpressionAttributeValues={
                    ':n': self.nome,
                    ':a': self.artista,
                    ':al': self.ano_lancamento,
                    ':e': self.estilo
                },
                ReturnValues="UPDATED_NEW"
            )
            return response

        except Exception:
            raise

    def remover(self, disco_id, dynamodb):
        try:
            if not disco_id(disco_id):
                return 'Código do disco ´obrigatório!'

            if not validar_disco_id(disco_id):
                return 'Código do disco inválido!'

            self.disco_id = disco_id

            table = dynamodb.Table(self.tabela)

            disco = self.obter_por_id(self.disco_id, dynamodb)
            if disco.__contains__('Erro:'):
                return disco

            response = table.delete_item(
                Key={
                    'pk': 'DISCOS#' + str(self.disco_id),
                    'sk': 'DISCO'
                }
            )
            return response
        except Exception as ex:
            raise ex

    def repor_estoque_disco(self, disco_id, quantidade, dynamodb):
        try:
            if not disco_id:
                return 'Código do disco é obrigatório!'

            if not validar_disco_id(disco_id):
                return 'Código do disco inválido!'

            if not quantidade:
                return 'Quantidade ´é obrigatória!'

            if not validar_quantidade(quantidade):
                return 'Quantidade inválida!'

            self.disco_id = disco_id
            self.quantidade = int(quantidade)

            disco = self.obter_por_id(self.disco_id, dynamodb)
            if disco.__contains__('Erro:'):
                return disco

            table = dynamodb.Table(self.tabela)

            response = table.update_item(
                Key={
                    'pk': 'DISCOS#' + str(self.disco_id),
                    'sk': 'DISCO'
                },
                UpdateExpression="set nome=:n, artista=:a, ano_lancamento=:al, estilo=:e",
                ExpressionAttributeValues={
                    ':n': self.nome,
                    ':a': self.artista,
                    ':al': self.ano_lancamento,
                    ':e': self.estilo
                },
                ReturnValues="UPDATED_NEW"
            )
            return response

        except Exception:
            raise
